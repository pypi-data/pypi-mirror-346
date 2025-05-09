import abc
from dataclasses import dataclass

from petsc4py import PETSc

import basix
import dolfinx
import ufl
from dolfinx import la

import scifem

from .geometry import BaseGeometry

QUAD_DEGREE = 8


def build_nullspace(V: dolfinx.fem.FunctionSpace):
    """Build PETSc nullspace for 3D elasticity"""

    # Create vectors that will span the nullspace
    bs = V.dofmap.index_map_bs
    length0 = V.dofmap.index_map.size_local
    basis = [
        la.vector(V.dofmap.index_map, bs=bs, dtype=dolfinx.default_scalar_type) for i in range(6)
    ]
    b = [b.array for b in basis]

    # Get dof indices for each subspace (x, y and z dofs)
    dofs = [V.sub(i).dofmap.list.flatten() for i in range(3)]

    # Set the three translational rigid body modes
    for i in range(3):
        b[i][dofs[i]] = 1.0

    # Set the three rotational rigid body modes
    x = V.tabulate_dof_coordinates()
    dofs_block = V.dofmap.list.flatten()
    x0, x1, x2 = x[dofs_block, 0], x[dofs_block, 1], x[dofs_block, 2]
    b[3][dofs[0]] = -x1
    b[3][dofs[1]] = x0
    b[4][dofs[0]] = x2
    b[4][dofs[2]] = -x0
    b[5][dofs[2]] = x1
    b[5][dofs[1]] = -x2

    la.orthonormalize(basis)

    basis_petsc = [
        PETSc.Vec().createWithArray(x[: bs * length0], bsize=3, comm=V.mesh.comm)  # type: ignore
        for x in b
    ]
    return PETSc.NullSpace().create(vectors=basis_petsc)  # type: ignore


@dataclass
class Material(abc.ABC):
    geo: BaseGeometry

    def __post_init__(self):
        P_u = basix.ufl.element(
            family="Lagrange",
            cell=str(self.geo.mesh.ufl_cell()),
            degree=2,
            shape=(self.geo.mesh.geometry.dim,),
        )
        self.u_space = dolfinx.fem.functionspace(self.geo.mesh, P_u)
        P_p = basix.ufl.element(
            family="Lagrange",
            cell=str(self.geo.mesh.ufl_cell()),
            degree=1,
            shape=(),
        )
        p_space = dolfinx.fem.functionspace(self.geo.mesh, P_p)

        self.u = dolfinx.fem.Function(self.u_space, name="u")
        self.v = ufl.TestFunction(self.u_space)
        self.du = ufl.TrialFunction(self.u_space)
        self.p = dolfinx.fem.Function(p_space, name="p")
        self.q = ufl.TestFunction(p_space)
        self.dp = ufl.TrialFunction(p_space)

        # self.create_solver()

    @property
    def comm(self):
        return self.geo.mesh.comm

    @property
    def ds(self):
        return ufl.Measure(
            "ds",
            domain=self.geo.mesh,
            subdomain_data=self.geo.facet_tags,
            metadata={"quadrature_degree": QUAD_DEGREE},
        )

    @property
    def dx(self):
        return ufl.Measure(
            "dx",
            domain=self.geo.mesh,
            metadata={"quadrature_degree": QUAD_DEGREE},
        )

    @property
    @abc.abstractmethod
    def bcs(self) -> list[dolfinx.fem.dirichletbc]: ...

    @property
    def N(self):
        return ufl.FacetNormal(self.geo.mesh)

    @abc.abstractmethod
    def neumann(self, A): ...

    @abc.abstractmethod
    def robin(self, A): ...

    def create_solver(self, G):
        F = self.F
        A = F * ufl.inv(G)
        P = self.P(A)
        dx = ufl.dx(metadata={"quadrature_degree": QUAD_DEGREE})
        elasticity_term = ufl.inner(P, ufl.grad(self.v)) * dx
        pressure_term = self.q * (ufl.det(A) - 1) * dx

        F0 = elasticity_term + self.robin(A) + self.neumann(A)
        F1 = pressure_term

        R = [F0, F1]
        dR = [
            [ufl.derivative(F0, self.u, self.du), ufl.derivative(F0, self.p, self.dp)],
            [ufl.derivative(F1, self.u, self.du), ufl.derivative(F1, self.p, self.dp)],
        ]

        petsc_options = {
            "ksp_type": "preonly",
            "pc_type": "lu",
            "pc_factor_mat_solver_type": "mumps",
            "ksp_monitor": None,
        }
        self.solver = scifem.NewtonSolver(
            R,
            dR,
            [self.u, self.p],
            bcs=self.bcs,
            max_iterations=25,
            petsc_options=petsc_options,
        )
        null_space = build_nullspace(self.u_space)
        self.solver.A.setNearNullSpace(null_space)

    def P(self, F):
        # F = ufl.variable(F)
        J = ufl.det(F)
        mu = dolfinx.fem.Constant(self.geo.mesh, dolfinx.default_scalar_type(10.0))
        # I1 = ufl.tr(F.T * F)
        # psi = mu * (I1 - 3) / 2

        # # Stress and weak form
        # return ufl.diff(psi, F) + self.p * ufl.inv(F).T * J
        return mu * (F - ufl.inv(F).T) - self.p * ufl.inv(F).T * J

    @property
    def F(self):
        return ufl.Identity(3) + ufl.grad(self.u)

    def sigma(self, F):
        return self.P(F) * F.T / ufl.det(F)

    def solve(self, G) -> int:
        self.create_solver(G)
        return self.solver.solve()


class CubeMaterial(Material):
    def __post_init__(self):
        self.x_displacement = dolfinx.fem.Constant(self.geo.mesh, 0.0)
        return super().__post_init__()

    @property
    def bcs(self):
        # Dirichlet boundary conditions
        fdim = 2
        zmin_facets = self.geo.facet_tags.find(self.geo.markers["ZMIN"][0])
        zmin_dofs = dolfinx.fem.locate_dofs_topological(self.u_space.sub(2), fdim, zmin_facets)
        ymin_facets = self.geo.facet_tags.find(self.geo.markers["YMIN"][0])
        ymin_dofs = dolfinx.fem.locate_dofs_topological(self.u_space.sub(1), fdim, ymin_facets)
        xmin_facets = self.geo.facet_tags.find(self.geo.markers["XMIN"][0])
        xmin_dofs = dolfinx.fem.locate_dofs_topological(self.u_space.sub(0), fdim, xmin_facets)
        x_max_facets = self.geo.facet_tags.find(self.geo.markers["XMAX"][0])
        x_max_dofs = dolfinx.fem.locate_dofs_topological(self.u_space.sub(0), fdim, x_max_facets)

        bc_zmin = dolfinx.fem.dirichletbc(0.0, zmin_dofs, self.u_space.sub(2))
        bc_ymin = dolfinx.fem.dirichletbc(0.0, ymin_dofs, self.u_space.sub(1))
        bc_xmin = dolfinx.fem.dirichletbc(0.0, xmin_dofs, self.u_space.sub(0))
        bc_xmax = dolfinx.fem.dirichletbc(self.x_displacement, x_max_dofs, self.u_space.sub(0))

        return [bc_zmin, bc_ymin, bc_xmin, bc_xmax]

    def neumann(self, A):
        return 0.0

    def robin(self, A):
        return 0.0


class CylinderMaterial(Material):
    def __post_init__(self):
        self.pressure = dolfinx.fem.Constant(self.geo.mesh, dolfinx.default_scalar_type(0.0))
        self.spring = dolfinx.fem.Constant(self.geo.mesh, dolfinx.default_scalar_type(1.0))
        super().__post_init__()

    @property
    def bcs(self):
        # Dirichlet boundary conditions
        fdim = 2
        bottom_facets = self.geo.facet_tags.find(self.geo.markers["BOTTOM"][0])
        bottom_dofs = dolfinx.fem.locate_dofs_topological(self.u_space.sub(2), fdim, bottom_facets)

        top_facets = self.geo.facet_tags.find(self.geo.markers["TOP"][0])
        top_dofs = dolfinx.fem.locate_dofs_topological(self.u_space.sub(2), fdim, top_facets)

        # Clamped boundary conditions on the bottom and top surfaces
        bc_bottom = dolfinx.fem.dirichletbc(0.0, bottom_dofs, self.u_space.sub(2))
        bc_top = dolfinx.fem.dirichletbc(0.0, top_dofs, self.u_space.sub(2))
        return [bc_bottom, bc_top]

    def neumann(self, A):
        # Pressure on the inside (Neumann)
        return ufl.inner(self.v, self.pressure * ufl.det(A) * ufl.inv(A).T * self.N) * self.ds(
            self.geo.markers["INSIDE"][0],
        )

    def robin(self, A):
        # Robin on the outside
        robin_value = ufl.inner(self.spring * self.u, self.N)
        return ufl.inner(robin_value * self.v, ufl.det(A) * ufl.inv(A).T * self.N) * self.ds(
            self.geo.markers["OUTSIDE"][0],
        )
