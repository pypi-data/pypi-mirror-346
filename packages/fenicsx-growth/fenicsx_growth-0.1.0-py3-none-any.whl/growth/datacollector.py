import logging
from collections import defaultdict
from pathlib import Path

import dolfinx
import matplotlib.pyplot as plt
import numpy as np

import scifem

logger = logging.getLogger(__name__)


class DataCollector:
    def __init__(
        self,
        points: np.ndarray,
        outfolder: Path = Path("results"),
    ):
        self.outfolder = outfolder
        self.outfolder.mkdir(parents=True, exist_ok=True)
        logger.info(f"Output directory: {self.outfolder}")

        self.writer = None
        self.points = points
        self.functions: dict[str, dolfinx.fem.Function] = {}
        self.history: dict[str, list[float]] = {}
        self.time: list[float] = []

    def register_function(self, name: str, function: dolfinx.fem.Function):
        function.name = name

        self.functions[name] = function
        if name not in self.history:
            self.history[name] = []

    def setup(self):
        assert len(self.functions) > 0, "No functions registered for output"

        # We can only save fuctions from the same function space
        # in a vtx file
        sorted_fuctions = defaultdict(list)
        for f in self.functions.values():
            f_hash = f.function_space.element.basix_element.hash()
            sorted_fuctions[f_hash].append(f)

        # Grab the communicator from the first function
        n = 1
        self.writers = []
        comm = self.functions[list(self.functions.keys())[0]].function_space.mesh.comm
        for funcs in sorted_fuctions.values():
            if len(funcs) == 1:
                # If we have only one function, we can use its name
                filename = self.outfolder / f"{funcs[0].name}.bp"
            else:
                filename = self.outfolder / f"variables_{n}.bp"
                n += 1

            self.writers.append(
                dolfinx.io.VTXWriter(
                    comm,
                    filename,
                    funcs,
                    engine="BP4",
                ),
            )

    def write(self, t):
        logger.info(f"Writing data at time {t}")
        for writer in self.writers:
            writer.write(t)

        self.time.append(t)
        for name, function in self.functions.items():
            logger.debug(f"Evaluating function {name}")
            values = scifem.evaluate_function(function, self.points)
            logger.debug(f"Evaluated function {name} at points {self.points}, values {values}")
            self.history[name].append(values)
        self.save_history()
        self.plot()

    def save_history(self):
        logger.info("Saving history")
        for name, values in self.history.items():
            np.save(self.outfolder / f"{name}.npy", np.array(values))
        np.save(self.outfolder / "time.npy", np.array(self.time))
        logger.debug(f"Saved data to {self.outfolder}")

    def plot_all(self):
        fig, ax = plt.subplots(len(self.history), 1, figsize=(8, 8), sharex=True)
        for i, (name, values) in enumerate(self.history.items()):
            for j, point in enumerate(self.points):
                label = f"({point[0]:.1f}, {point[1]:.1f}, {point[2]:.1f})"
                ax[i].plot(self.time, np.array(list(zip(*values)))[j], label=label)
            ax[i].legend()
            ax[i].set_ylabel(name)
            ax[i].set_title(name)
            ax[i].grid()
        ax[i].set_xlabel("Time")
        fig.savefig(self.outfolder / "variables.png")
        plt.close(fig)

    def plot(self):
        logger.info("Plotting data")
        fig, ax = plt.subplots(len(self.points), figsize=(12, 8), sharex=True)
        for j, point in enumerate(self.points):
            label = f"({point[0]:.1f}, {point[1]:.1f}, {point[2]:.1f})"

            (l1,) = ax[j].plot(
                self.time,
                np.array(list(zip(*self.history["stress"])))[j],
                label="stress",
                linestyle="-",
                marker="o",
                color="r",
            )
            (l2,) = ax[j].plot(
                self.time,
                np.array(list(zip(*self.history["setpoint"])))[j],
                label="setpoint",
                linestyle="--",
                color="g",
            )
            ax2 = ax[j].twinx()
            (l3,) = ax2.plot(
                self.time,
                np.array(list(zip(*self.history["g_cum"])))[j],
                linestyle="-",
                marker="o",
                color="b",
            )
            ax2.set_ylabel("growth")
            (l4,) = ax2.plot(
                self.time,
                np.array(list(zip(*self.history["g_incr"])))[j],
                linestyle="-",
                marker="o",
                color="m",
            )

            ax[j].legend((l1, l2, l3, l4), ("stress", "setpoint", "g_cum", "g_incr"))
            ax[j].set_ylabel("stress")
            ax[j].set_title(label)
            ax[j].grid()
        ax[j].set_xlabel("Time")
        logger.debug(f"Saving plot to {self.outfolder / 'variables_points.png'}")
        fig.savefig(self.outfolder / "variables_points.png")
        plt.close(fig)
