from __future__ import annotations

import logging

from mpi4py import MPI

import dolfinx
import matplotlib.pyplot as plt
import numpy as np
import ufl

from ..datacollector import DataCollector
from ..growth import GrowthModel, GrowthTensor
from ..material import Material

logger = logging.getLogger(__name__)


class SimpleStressGrowthModel(GrowthModel):
    def __init__(
        self,
        model: Material,
        collector: DataCollector,
        parameters: dict[str, float] | None = None,
        setpoint: float | dolfinx.fem.Function = 0.0,
        use_full_growth_tensor: bool = False,
    ):
        super().__init__(model, collector, parameters)
        self.g_cum_ff = dolfinx.fem.Function(self.scalar_growth_space, name="g_cum_ff")
        self.g_cum_ff.x.array[:] = 1.0
        self.g_cum_tt = dolfinx.fem.Function(self.scalar_growth_space, name="g_cum_tt")
        self.g_cum_tt.x.array[:] = 1.0

        self.g_incr_ff = dolfinx.fem.Function(self.scalar_growth_space, name="g_incr_ff")
        self.g_incr_ff.x.array[:] = 1.0
        self.g_incr_tt = dolfinx.fem.Function(self.scalar_growth_space, name="g_incr_tt")
        self.g_incr_tt.x.array[:] = 1.0

        self.stress = dolfinx.fem.Function(self.scalar_growth_space, name="stress")
        self.stress.x.array[:] = 0.0

        self.collector.register_function("g_cum_ff", self.g_cum_ff)
        self.collector.register_function("g_cum_tt", self.g_cum_tt)
        self.collector.register_function("g_incr_ff", self.g_incr_ff)
        self.collector.register_function("g_incr_tt", self.g_incr_tt)
        self.collector.register_function("stress", self.stress)

        # self.collector.register_function("s_t", self.st)
        self.collector.register_function("u", self.model.u)

        self.collector.setup()

        self.growth_tensor = GrowthTensor(
            f=self.geo.f,
            g_ff=self.g_incr_ff,
            g_tt=self.g_incr_tt,
        )

        self.G_update_expr = dolfinx.fem.Expression(
            self.growth_tensor.tensor(),
            self.Q.element.interpolation_points(),
        )

        # F_tot = A_tot * G_tot
        # Cauchy stress
        self.T_tot = dolfinx.fem.Function(self.Q)

        if isinstance(setpoint, dolfinx.fem.Function):
            self.setpoint = setpoint
        else:
            self.setpoint = dolfinx.fem.Constant(
                self.geo.mesh,
                dolfinx.default_scalar_type(setpoint),
            )

        self.T_tot_expr = dolfinx.fem.Expression(
            self.model.sigma(self.A_tot),
            self.Q.element.interpolation_points(),
        )
        self.T_tot.interpolate(self.T_tot_expr)

        self.collector.write(-1.0)

    def init(self):
        self.model.solve(G=self.G_tot)
        self.F.interpolate(
            dolfinx.fem.Expression(
                ufl.Identity(3) + ufl.grad(self.model.u),
                self.Q.element.interpolation_points(),
            ),
        )
        self.A_tot.interpolate(self.A_tot_expr)
        self.T_tot.interpolate(self.T_tot_expr)

        self.collector.write(0.0)

    def solve(self, T: float, dt: float, save_freq: int = 10):
        # We grow in the transverse direction
        g_incr_tt_expr = dolfinx.fem.Expression(
            1 + dt * (self.stress - self.setpoint),
            self.scalar_growth_space.element.interpolation_points(),
        )
        stress_expr = dolfinx.fem.Expression(
            ufl.inner(self.T_tot * self.geo.s, self.geo.s),
            self.scalar_growth_space.element.interpolation_points(),
        )
        self.stress.interpolate(stress_expr)
        g_cum_tt_expr = dolfinx.fem.Expression(
            ufl.inner(self.G_tot * self.geo.f, self.geo.f),
            self.scalar_growth_space.element.interpolation_points(),
        )

        vol = self.comm.allreduce(
            dolfinx.fem.assemble_scalar(
                dolfinx.fem.form(dolfinx.fem.Constant(self.geo.mesh, 1.0) * ufl.dx),
            ),
            op=MPI.SUM,
        )
        stimuli_form = dolfinx.fem.form((self.stress - self.setpoint) * ufl.dx)

        time = np.arange(0, T + dt, dt)

        for i, t in enumerate(time[1:]):
            self.g_incr_tt.interpolate(g_incr_tt_expr)
            self.G.interpolate(self.G_update_expr)
            self.G_tot.interpolate(self.G_tot_expr)
            self.g_cum_tt.interpolate(g_cum_tt_expr)

            if self.comm.rank == 0:
                logger.info(f"Iteration {i}")

            self.model.solve(G=self.G_tot)

            self.A_tot.interpolate(self.A_tot_expr)
            self.T_tot.interpolate(self.T_tot_expr)
            self.stress.interpolate(stress_expr)
            if i % save_freq == 0:
                self.collector.write(t)

            stimuli = (
                self.comm.allreduce(dolfinx.fem.assemble_scalar(stimuli_form), op=MPI.SUM) / vol
            )
            logger.info(f"Total stimuli = {stimuli}")
            if abs(stimuli) < 1e-4:
                logger.info("Stopping growth")
                break


class SimpleStressDataCollector(DataCollector):
    def plot(self):
        logger.info("Plotting data")
        fig, ax = plt.subplots(len(self.points), 2, figsize=(12, 8), sharex=True)
        for j, point in enumerate(self.points):
            label = f"({point[0]:.1f}, {point[1]:.1f}, {point[2]:.1f})"

            (l1,) = ax[j, 0].plot(
                self.time,
                np.array(list(zip(*self.history["g_cum_tt"])))[j],
                linestyle="-",
                color="r",
            )
            (l2,) = ax[j, 0].plot(
                self.time,
                np.array(list(zip(*self.history["g_incr_tt"])))[j],
                linestyle="-",
                color="g",
            )
            (l3,) = ax[j, 1].plot(
                self.time,
                np.array(list(zip(*self.history["stress"])))[j],
                linestyle="-",
                color="r",
            )

            ax[j, 0].legend((l1, l2), ("g_cum_tt", "g_incr_tt"))
            ax[j, 0].set_ylabel("Growth")
            ax[j, 0].set_title(label)
            ax[j, 0].grid()

            ax[j, 1].legend((l3,), ("stress",))
            ax[j, 1].set_ylabel("Stress")
            ax[j, 1].set_title(label)
            ax[j, 1].grid()
        ax[j, 0].set_xlabel("Time")
        logger.debug(f"Saving plot to {self.outfolder / 'variables_points.png'}")
        fig.savefig(self.outfolder / "variables_points.png")
        plt.close(fig)
