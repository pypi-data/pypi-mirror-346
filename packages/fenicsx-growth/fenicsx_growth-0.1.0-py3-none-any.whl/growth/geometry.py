import shutil
from pathlib import Path
from typing import NamedTuple

from mpi4py import MPI

import basix
import dolfinx
import gmsh
import numpy as np
import ufl


def get_cylinder_fibers(mesh, fiber_el, rotate=False):
    fiber_space = dolfinx.fem.functionspace(mesh, fiber_el)

    X = ufl.SpatialCoordinate(mesh)

    fiber_r = dolfinx.fem.Function(fiber_space, name="fiber_r")
    fiber_ang = dolfinx.fem.Function(fiber_space, name="fiber_ang")
    fiber_z = dolfinx.fem.Function(fiber_space, name="fiber_z")

    fiber_r_expr = ufl.as_vector(
        [
            X[0] / ufl.sqrt(X[0] ** 2 + X[1] ** 2),
            X[1] / ufl.sqrt(X[0] ** 2 + X[1] ** 2),
            0,
        ],
    )
    fiber_r.interpolate(
        dolfinx.fem.Expression(fiber_r_expr, fiber_space.element.interpolation_points()),
    )

    fiber_ang_expr = ufl.as_vector(
        [
            X[1] / ufl.sqrt(X[0] ** 2 + X[1] ** 2),
            -X[0] / ufl.sqrt(X[0] ** 2 + X[1] ** 2),
            0,
        ],
    )
    fiber_z_expr = dolfinx.fem.Constant(mesh, (0, 0, 1.0))
    if rotate:
        arg = (ufl.sqrt(X[0] ** 2 + X[1] ** 2) - 10) / 10
        fiber_ang_expr = fiber_ang_expr * ufl.cos(arg) - fiber_z_expr * ufl.sin(arg)
        fiber_z_expr = fiber_ang_expr * ufl.sin(arg) + fiber_z_expr * ufl.cos(arg)

    fiber_z.interpolate(
        dolfinx.fem.Expression(fiber_z_expr, fiber_space.element.interpolation_points()),
    )
    fiber_ang.interpolate(
        dolfinx.fem.Expression(fiber_ang_expr, fiber_space.element.interpolation_points()),
    )

    return fiber_r, fiber_ang, fiber_z


def get_cube_fibers(mesh, fiber_el):
    fiber_space = dolfinx.fem.functionspace(mesh, fiber_el)

    fiber_x = dolfinx.fem.Function(fiber_space, name="fiber_r")
    fiber_y = dolfinx.fem.Function(fiber_space, name="fiber_ang")
    fiber_z = dolfinx.fem.Function(fiber_space, name="fiber_z")

    fiber_x_expr = dolfinx.fem.Constant(mesh, (1.0, 0.0, 0.0))
    fiber_x.interpolate(
        dolfinx.fem.Expression(fiber_x_expr, fiber_space.element.interpolation_points()),
    )
    fiber_y_expr = dolfinx.fem.Constant(mesh, (0.0, 1.0, 0.0))
    fiber_y.interpolate(
        dolfinx.fem.Expression(fiber_y_expr, fiber_space.element.interpolation_points()),
    )
    fiber_z_expr = dolfinx.fem.Constant(mesh, (0.0, 0.0, 1.0))
    fiber_z.interpolate(
        dolfinx.fem.Expression(fiber_z_expr, fiber_space.element.interpolation_points()),
    )
    return fiber_x, fiber_y, fiber_z


class BaseGeometry(NamedTuple):
    mesh: dolfinx.mesh.Mesh
    facet_tags: dolfinx.mesh.MeshTags
    f: dolfinx.fem.Function
    s: dolfinx.fem.Function
    n: dolfinx.fem.Function
    markers: dict[str, tuple[int, int]]

    def save(self, output_dir: Path) -> None:
        """Save the geometry to a file."""
        # Save the mesh
        with dolfinx.io.XDMFFile(self.mesh.comm, output_dir / "mesh.xdmf", "w") as xdmf:
            xdmf.write_mesh(self.mesh)
            xdmf.write_meshtags(self.facet_tags, self.mesh.geometry)

        # Save the fiber fields
        save_fibers(self, output_dir)


class CubeGeometry(BaseGeometry):
    @property
    def x_range(self) -> tuple[float, float]:
        comm = self.mesh.comm
        min_value = comm.allreduce(self.mesh.geometry.x[:, 0].min(), op=MPI.MIN)
        max_value = comm.allreduce(self.mesh.geometry.x[:, 0].max(), op=MPI.MAX)
        return min_value, max_value

    @property
    def y_range(self) -> tuple[float, float]:
        comm = self.mesh.comm
        min_value = comm.allreduce(self.mesh.geometry.x[:, 1].min(), op=MPI.MIN)
        max_value = comm.allreduce(self.mesh.geometry.x[:, 1].max(), op=MPI.MAX)
        return min_value, max_value

    @property
    def z_range(self) -> tuple[float, float]:
        comm = self.mesh.comm
        min_value = comm.allreduce(self.mesh.geometry.x[:, 2].min(), op=MPI.MIN)
        max_value = comm.allreduce(self.mesh.geometry.x[:, 2].max(), op=MPI.MAX)
        return min_value, max_value


class CylinderGeometry(BaseGeometry):
    @property
    def z_range(self) -> tuple[float, float]:
        comm = self.mesh.comm
        min_value = comm.allreduce(self.mesh.geometry.x[:, 2].min(), op=MPI.MIN)
        max_value = comm.allreduce(self.mesh.geometry.x[:, 2].max(), op=MPI.MAX)
        return min_value, max_value

    @property
    def r_range(self) -> tuple[float, float]:
        # Get the minimum and maximum values of the radial coordinate
        comm = self.mesh.comm
        r = self.mesh.geometry.x[:, 0] ** 2 + self.mesh.geometry.x[:, 1] ** 2
        min_value = comm.allreduce(r.min(), op=MPI.MIN)
        max_value = comm.allreduce(r.max(), op=MPI.MAX)
        return np.sqrt(min_value), np.sqrt(max_value)

    @property
    def theta_range(self) -> tuple[float, float]:
        # Get the minimum and maximum values of the angular coordinate
        comm = self.mesh.comm
        theta = np.arctan2(self.mesh.geometry.x[:, 1], self.mesh.geometry.x[:, 0])
        min_value = comm.allreduce(theta.min(), op=MPI.MIN)
        max_value = comm.allreduce(theta.max(), op=MPI.MAX)
        return min_value, max_value


def save_fibers(geo: BaseGeometry, output_dir: Path) -> None:
    shutil.rmtree(output_dir / "fibers.bp", ignore_errors=True)
    with dolfinx.io.VTXWriter(
        MPI.COMM_WORLD,
        output_dir / "fibers.bp",
        [geo.f, geo.s, geo.n],
        engine="BP4",
    ) as vtx:
        vtx.write(0.0)


def create_cylindrical_mesh(
    inner_radius=10.0,
    outer_radius=20.0,
    height=40.0,
    char_length=10.0,
    mesh_name="cylinder.msh",
    verbose=True,
):
    """Create a thick cylindrical shell (hollow cylinder) mesh using GMSH

    Parameters:
        inner_radius: Inner radius of the shell (mm)
        outer_radius: Outer radius of the shell (mm)
        height: Height of the cylinder (mm)
        char_length: Characteristic mesh element size (mm)
        mesh_name: Name of the output mesh file (without extension)
        verbose: Whether to print GMSH output
        save_xdmf: Whether to also save the mesh in XDMF format for ParaView
    """
    gmsh.initialize()
    if not verbose:
        gmsh.option.setNumber("General.Verbosity", 0)
    gmsh.model.add(mesh_name)

    # Create two concentric cylinders
    outer_cylinder = gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, height, outer_radius)
    inner_cylinder = gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, height, inner_radius)

    # Boolean subtraction to get the shell
    outer = [(3, outer_cylinder)]
    inner = [(3, inner_cylinder)]
    shell, id = gmsh.model.occ.cut(outer, inner, removeTool=True)

    gmsh.model.occ.synchronize()

    # Get all surfaces to identify them
    surfaces = gmsh.model.occ.getEntities(dim=2)

    gmsh.model.addPhysicalGroup(
        dim=surfaces[0][0],
        tags=[surfaces[0][1]],
        tag=1,
        name="INSIDE",
    )
    gmsh.model.addPhysicalGroup(
        dim=surfaces[1][0],
        tags=[surfaces[1][1]],
        tag=2,
        name="OUTSIDE",
    )
    gmsh.model.addPhysicalGroup(
        dim=surfaces[2][0],
        tags=[surfaces[2][1]],
        tag=3,
        name="TOP",
    )
    gmsh.model.addPhysicalGroup(
        dim=surfaces[3][0],
        tags=[surfaces[3][1]],
        tag=4,
        name="BOTTOM",
    )

    gmsh.model.addPhysicalGroup(dim=3, tags=[t[1] for t in shell], tag=5, name="VOLUME")

    # Set mesh size
    gmsh.option.setNumber("Mesh.CharacteristicLengthMin", char_length)
    gmsh.option.setNumber("Mesh.CharacteristicLengthMax", char_length)

    # Generate mesh
    gmsh.model.mesh.generate(3)
    gmsh.model.mesh.optimize("Netgen")

    # gmsh.option.setNumber("Mesh.SaveAll", 1)

    # Write mesh to file
    path = Path(mesh_name).with_suffix(".msh")
    gmsh.write(path.as_posix())

    # Finalize GMSH
    gmsh.finalize()

    print(f"Cylindrical shell mesh generated and saved to {mesh_name}")

    return path


def load_cylinder_geometry(comm: MPI.Intracomm, rotate_fibers: bool = True) -> CylinderGeometry:
    mesh_filename = Path("cylindrical.msh")
    if not mesh_filename.exists():
        mesh_filename = create_cylindrical_mesh()

    if comm.rank == 0:
        gmsh.initialize()
        gmsh.model.add("Mesh from file")
        gmsh.merge(str(mesh_filename))
        mesh, cell_tags, facet_tags = dolfinx.io.gmshio.model_to_mesh(gmsh.model, comm, 0)
        markers = {
            gmsh.model.getPhysicalName(*v): tuple(reversed(v))
            for v in gmsh.model.getPhysicalGroups()
        }
        gmsh.finalize()
    else:
        mesh, cell_tags, facet_tags = dolfinx.io.gmshio.model_to_mesh(gmsh.model, comm, 0)
        markers = {}

    markers = comm.bcast(markers, root=0)

    fiber_el = basix.ufl.element(
        family="Lagrange",
        cell=str(mesh.ufl_cell()),
        degree=1,
        shape=(mesh.geometry.dim,),
        discontinuous=True,
    )
    fiber_r, fiber_ang, fiber_z = get_cylinder_fibers(mesh, fiber_el, rotate=rotate_fibers)

    return CylinderGeometry(
        mesh=mesh,
        facet_tags=facet_tags,
        f=fiber_r,
        s=fiber_ang,
        n=fiber_z,
        markers=markers,
    )


def load_cube_geometry(comm: MPI.Intracomm) -> CubeGeometry:
    x_min, x_max, Nx = 0, 1, 4
    y_min, y_max, Ny = 0, 1, 4
    z_min, z_max, Nz = 0, 1, 4

    mesh = dolfinx.mesh.create_box(
        comm,
        [np.array([x_min, y_min, z_min]), np.array([x_max, y_max, z_max])],
        [Nx, Ny, Nz],
        cell_type=dolfinx.mesh.CellType.tetrahedron,
    )

    bcs_func = dict(
        XMIN=lambda x: np.isclose(x[0], x_min),
        XMAX=lambda x: np.isclose(x[0], x_max),
        YMIN=lambda x: np.isclose(x[1], y_min),
        YMAX=lambda x: np.isclose(x[1], y_max),
        ZMIN=lambda x: np.isclose(x[2], z_min),
        ZMAX=lambda x: np.isclose(x[2], z_max),
    )
    points = []
    values = []
    markers = {}
    for i, (name, f) in enumerate(bcs_func.items(), start=1):
        facet_points = dolfinx.mesh.locate_entities_boundary(mesh, mesh.topology.dim - 1, f)
        points.append(facet_points)
        values.append(np.full_like(facet_points, i))
        markers[name] = (i, 2)

    facet_tags = dolfinx.mesh.meshtags(
        mesh,
        mesh.topology.dim - 1,
        np.hstack(points),
        np.hstack(values).astype(np.int32),
    )

    # Create fiber field
    fiber_el = basix.ufl.element(
        family="Lagrange",
        cell=str(mesh.ufl_cell()),
        degree=1,
        shape=(mesh.geometry.dim,),
        discontinuous=True,
    )
    fiber_x, fiber_y, fiber_z = get_cube_fibers(mesh, fiber_el)

    return CubeGeometry(
        mesh=mesh,
        facet_tags=facet_tags,
        f=fiber_x,
        s=fiber_y,
        n=fiber_z,
        markers=markers,
    )


if __name__ == "__main__":
    create_cylindrical_mesh()
