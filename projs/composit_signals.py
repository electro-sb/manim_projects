from manim import *

from manim import *
import numpy as np


class HarmonicSignal(Scene):
    def construct(self):
        # Parameters
        f0 = 1.0 #2.5  # fundamental frequency in Hz
        harmonics = [1, 3, 5, 7]  # harmonic multipliers
        duration = 20  # seconds
        sample_rate = 200  # points per second

        # Time array
        t = np.linspace(0, duration, int(sample_rate * duration))

        # Generate composite signal
        signal = np.zeros_like(t)
        for h in harmonics:
            signal += np.sin(2 * np.pi * f0 * h * t)

        # Normalize for plotting
        signal /= len(harmonics)

        # Axes
        axes = (
            Axes(
                x_range=[0, duration, 2],
                y_range=[-1.2, 1.2, 0.5],
                axis_config={"color": BLUE},
                tips=False,
            )
            .scale(0.9)
            .to_edge(DOWN)
        )

        labels = axes.get_axis_labels("t (s)", "Amplitude")

        # Create graph
        graph = axes.plot_line_graph(
            x_values=t, y_values=signal, line_color=YELLOW, add_vertex_dots=False
        )

        # Animate
        self.play(Create(axes), Write(labels))
        self.play(Create(graph), run_time=5, rate_func=linear)
        self.wait()

if __name__ == "__main__":
    from os import system

    system("manim -pql projs/composit_signals.py HarmonicSignal")
