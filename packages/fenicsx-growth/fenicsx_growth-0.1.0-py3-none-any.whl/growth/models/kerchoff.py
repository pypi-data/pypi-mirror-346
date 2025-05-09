from __future__ import annotations

import logging

from mpi4py import MPI

import dolfinx
import matplotlib.pyplot as plt
import numpy as np
import ufl

from ..datacollector import DataCollector
from ..growth import GrowthModel, GrowthTensor, identity_tensor
from ..material import Material

logger = logging.getLogger(__name__)


def k_growth(F_g_cum, slope, F_50):
    return 1 / (1 + ufl.exp(slope * (F_g_cum - F_50)))


def incr_fiber_growth(s_l, dt, F_l_cum, f_l_slope, F_ff50, f_ff_max, f_f, s_l50, **kwargs):
    k_ff = k_growth(F_l_cum, f_l_slope, F_ff50)
    frac_True = f_ff_max * dt / (1 + ufl.exp(-f_f * (s_l - s_l50)))
    frac_False = -f_ff_max * dt / (1 + ufl.exp(f_f * (s_l + s_l50)))
    return ufl.conditional(ufl.ge(s_l, 0.0), k_ff * frac_True + 1, frac_False + 1)


def incr_trans_growth(s_t, dt, F_c_cum, c_th_slope, F_cc50, f_cc_max, c_f, s_t50, **kwargs):
    k_cc = k_growth(F_c_cum, c_th_slope, F_cc50)
    frac_True = f_cc_max * dt / (1 + ufl.exp(-c_f * (s_t - s_t50)))
    frac_False = -f_cc_max * dt / (1 + ufl.exp(c_f * (s_t + s_t50)))

    return ufl.conditional(
        ufl.ge(s_t, 0.0),
        ufl.sqrt(k_cc * frac_True + 1),
        ufl.sqrt(frac_False + 1),
    )


class KerchoffGrowthModel(GrowthModel):
    def __init__(
        self,
        model: Material,
        collector: DataCollector,
        parameters: dict[str, float] | None = None,
        E_f_set: float | dolfinx.fem.Function = 0.0,
        E_c_set: float | dolfinx.fem.Function = 0.0,
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

        self.sl = dolfinx.fem.Function(self.scalar_growth_space, name="s_l")
        self.sl.x.array[:] = 1.0
        self.st = dolfinx.fem.Function(self.scalar_growth_space, name="s_t")
        self.st.x.array[:] = 1.0

        self.collector.register_function("g_cum_ff", self.g_cum_ff)
        self.collector.register_function("g_cum_tt", self.g_cum_tt)
        self.collector.register_function("g_incr_ff", self.g_incr_ff)
        self.collector.register_function("g_incr_tt", self.g_incr_tt)
        self.collector.register_function("s_l", self.sl)
        self.collector.register_function("s_t", self.st)
        self.collector.register_function("u", self.model.u)

        self.collector.setup()

        # if use_full_growth_tensor:
        #     # Add all microstructural growth directions
        #     self.growth_tensor = FullGrowthTensor(
        #         g_ff=self.g_incr_ff,
        #         f=self.geo.f,
        #         g_ss=self.g_incr_tt,
        #         s=self.geo.s,
        #         g_nn=self.g_incr_tt,
        #         n=self.geo.n,
        #     )
        # else:
        # Only fiber and transverse growth
        self.growth_tensor = GrowthTensor(
            f=self.geo.s,
            g_ff=self.g_incr_ff,
            g_tt=self.g_incr_tt,
        )

        self.G_update_expr = dolfinx.fem.Expression(
            self.growth_tensor.tensor(),
            self.Q.element.interpolation_points(),
        )

        # F_tot = A_tot * G_tot
        self.E_tot = dolfinx.fem.Function(self.Q)
        self.E_tot.interpolate(identity_tensor)

        if isinstance(E_f_set, dolfinx.fem.Function):
            self.E_f_set = E_f_set
        else:
            self.E_f_set = dolfinx.fem.Constant(self.geo.mesh, dolfinx.default_scalar_type(E_f_set))
        if isinstance(E_c_set, dolfinx.fem.Function):
            self.E_c_set = E_c_set
        else:
            self.E_c_set = dolfinx.fem.Constant(self.geo.mesh, dolfinx.default_scalar_type(E_c_set))

        self.sl_expr = dolfinx.fem.Expression(
            ufl.inner(self.E_tot * self.geo.f, self.geo.f) - self.E_f_set,
            self.scalar_growth_space.element.interpolation_points(),
        )
        self.st_expr = dolfinx.fem.Expression(
            ufl.inner(self.E_tot * self.geo.s, self.geo.s) - self.E_c_set,
            self.scalar_growth_space.element.interpolation_points(),
        )

        self.E_tot_expr = dolfinx.fem.Expression(
            0.5 * (self.A_tot.T * self.A_tot - ufl.Identity(3)),
            self.Q.element.interpolation_points(),
        )
        self.E_tot.interpolate(self.E_tot_expr)
        self.sl.interpolate(self.sl_expr)
        self.st.interpolate(self.st_expr)

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
        self.collector.write(0.0)

    @staticmethod
    def default_parameters():
        return {
            "f_ff_max": 0.3,
            "f_f": 150,
            "s_l50": 0.06,
            "F_ff50": 1.35,
            "f_l_slope": 40,
            "f_cc_max": 0.1,
            "c_f": 75,
            "s_t50": 0.07,
            "F_cc50": 1.28,
            "c_th_slope": 60,
        }

    def solve(self, T: float, dt: float, save_freq: int = 10):
        g_incr_ff_expr = dolfinx.fem.Expression(
            incr_fiber_growth(self.sl, dt, self.g_cum_ff, **self.parameters),
            self.scalar_growth_space.element.interpolation_points(),
        )
        g_incr_tt_expr = dolfinx.fem.Expression(
            incr_trans_growth(self.st, dt, self.g_cum_tt, **self.parameters),
            self.scalar_growth_space.element.interpolation_points(),
        )
        g_cum_ff_expr = dolfinx.fem.Expression(
            ufl.inner(self.G_tot * self.geo.f, self.geo.f),
            self.scalar_growth_space.element.interpolation_points(),
        )
        g_cum_tt_expr = dolfinx.fem.Expression(
            ufl.inner(self.G_tot * self.geo.s, self.geo.s),
            self.scalar_growth_space.element.interpolation_points(),
        )

        sl_form = dolfinx.fem.form(self.sl * ufl.dx)

        time = np.arange(0, T + dt, dt)

        for i, t in enumerate(time[1:]):
            self.g_incr_ff.interpolate(g_incr_ff_expr)
            self.g_incr_tt.interpolate(g_incr_tt_expr)
            self.G.interpolate(self.G_update_expr)
            self.G_tot.interpolate(self.G_tot_expr)
            self.g_cum_ff.interpolate(g_cum_ff_expr)
            self.g_cum_tt.interpolate(g_cum_tt_expr)

            if self.comm.rank == 0:
                logger.info(f"Iteration {i}")

            self.model.solve(G=self.G_tot)

            self.A_tot.interpolate(self.A_tot_expr)
            self.E_tot.interpolate(self.E_tot_expr)
            self.sl.interpolate(self.sl_expr)
            self.st.interpolate(self.st_expr)
            if i % save_freq == 0:
                self.collector.write(t)

            sl = self.comm.allreduce(dolfinx.fem.assemble_scalar(sl_form), op=MPI.SUM)
            logger.info(f"sl = {sl}")
            if abs(sl) < 1e-6:
                logger.info("Stopping growth")
                break


class KerchoffDataCollector(DataCollector):
    def plot(self):
        logger.info("Plotting data")
        fig, ax = plt.subplots(len(self.points), 2, figsize=(12, 8), sharex=True)
        for j, point in enumerate(self.points):
            label = f"({point[0]:.1f}, {point[1]:.1f}, {point[2]:.1f})"

            (l1,) = ax[j, 0].plot(
                self.time,
                np.array(list(zip(*self.history["g_cum_ff"])))[j],
                linestyle="-",
                color="r",
            )
            (l2,) = ax[j, 0].plot(
                self.time,
                np.array(list(zip(*self.history["g_cum_tt"])))[j],
                linestyle="-",
                color="g",
            )
            (l3,) = ax[j, 1].plot(
                self.time,
                np.array(list(zip(*self.history["s_l"])))[j],
                linestyle="-",
                color="r",
            )
            (l4,) = ax[j, 1].plot(
                self.time,
                np.array(list(zip(*self.history["s_t"])))[j],
                linestyle="-",
                color="g",
            )

            ax[j, 0].legend((l1, l2), ("g_cum_ff", "g_cum_tt"))
            ax[j, 0].set_ylabel("Cumulative growth")
            ax[j, 0].set_title(label)
            ax[j, 0].grid()

            ax[j, 1].legend((l3, l4), ("s_l", "s_t"))
            ax[j, 1].set_ylabel("Growth stimuli")
            ax[j, 1].set_title(label)
            ax[j, 1].grid()
        ax[j, 0].set_xlabel("Time")
        logger.debug(f"Saving plot to {self.outfolder / 'variables_points.png'}")
        fig.savefig(self.outfolder / "variables_points.png")
        plt.close(fig)
