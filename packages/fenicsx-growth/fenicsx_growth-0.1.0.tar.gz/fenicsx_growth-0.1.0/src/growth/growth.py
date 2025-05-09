from __future__ import annotations

import abc
from dataclasses import dataclass

import basix
import dolfinx
import numpy as np
import ufl

from .datacollector import DataCollector
from .material import Material


def identity_tensor(x):
    # utility function to create identity tensor
    values = np.zeros((9, x.shape[1]))
    values[0] = 1
    values[4] = 1
    values[8] = 1
    return values


# Based on eq (28) from https://www.sciencedirect.com/science/article/abs/pii/S1751616113003366
@dataclass
class GrowthTensor:
    g_ff: dolfinx.fem.Function
    f: dolfinx.fem.Function
    g_tt: dolfinx.fem.Function

    def tensor(self):
        return self.g_tt * ufl.Identity(3) - (self.g_ff - self.g_tt) * ufl.outer(self.f, self.f)


@dataclass
class FullGrowthTensor:
    g_ff: dolfinx.fem.Function
    f: dolfinx.fem.Function
    g_ss: dolfinx.fem.Function = None
    s: dolfinx.fem.Function = None
    g_nn: dolfinx.fem.Function = None
    n: dolfinx.fem.Function = None

    def tensor(self):
        return (
            self.g_ff * ufl.outer(self.f, self.f)
            + self.g_ss * ufl.outer(self.s, self.s)
            + self.g_nn * ufl.outer(self.n, self.n)
        )


class GrowthModel(abc.ABC):
    def __init__(
        self,
        model: Material,
        collector: DataCollector,
        parameters: dict[str, float] | None = None,
    ):
        self.parameters = self.default_parameters()
        if parameters is not None:
            self.parameters.update(parameters)
        self.model = model
        self.collector = collector

        scalar_element = basix.ufl.element(
            family="Lagrange",
            cell=str(self.geo.mesh.ufl_cell()),
            degree=1,
            shape=(),
            discontinuous=True,
        )
        self.scalar_growth_space = dolfinx.fem.functionspace(self.geo.mesh, scalar_element)
        self.Q = dolfinx.fem.functionspace(self.geo.mesh, ("DG", 1, (3, 3)))
        self.G = dolfinx.fem.Function(self.Q, name="G")
        self.G.interpolate(identity_tensor)

        self.A_tot = dolfinx.fem.Function(self.Q)
        self.A_tot.interpolate(identity_tensor)
        self.G_tot = dolfinx.fem.Function(self.Q)
        self.G_tot.interpolate(identity_tensor)
        self.F = dolfinx.fem.Function(self.Q)
        self.F.interpolate(identity_tensor)

        # Define expressions for updating cumulative tensors
        # See Goriely and Ben Amar (2007)
        # self.G_tot_expr = dolfinx.fem.Expression(
        #     ufl.inv(self.A_tot) * self.G * self.A_tot * self.G_tot,
        #     self.Q.element.interpolation_points(),
        # )
        self.G_tot_expr = dolfinx.fem.Expression(
            self.G * self.G_tot,
            self.Q.element.interpolation_points(),
        )
        self.A_tot_expr = dolfinx.fem.Expression(
            self.F * ufl.inv(self.G_tot),
            self.Q.element.interpolation_points(),
        )

    @property
    def comm(self):
        return self.model.comm

    @staticmethod
    def default_parameters():
        return {}

    @property
    def geo(self):
        return self.model.geo

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def solve(self, T: float, dt: float, save_freq: int = 10):
        pass
