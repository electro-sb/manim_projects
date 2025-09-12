from manim import *
import numpy as np


class ScrollingHarmonics(Scene):
    def construct(self):
        # Parameters
        f0 = 0.5 #2.5  # fundamental frequency in Hz
        harmonics = [1, 3, 5, 7]  # harmonic multipliers
        duration = 20  # total animation time in seconds
        window_width = 4  # seconds visible on screen at once
        sample_rate = 200  # points per second

        # Axes
        axes = (
            Axes(
                x_range=[0, window_width, 1],
                y_range=[-1.2, 1.2, 0.5],
                axis_config={"color": BLUE},
                tips=False,
            )
            .scale(0.9)
            .to_edge(DOWN)
        )

        labels = axes.get_axis_labels("t (s)", "Amplitude")
        self.play(Create(axes), Write(labels))

        # ValueTracker for time
        t_tracker = ValueTracker(0)

        # Function to generate composite signal up to current time
        def get_signal():
            t0 = t_tracker.get_value()
            t_vals = np.linspace(t0, t0 + window_width, int(sample_rate * window_width))
            signal = np.zeros_like(t_vals)
            for h in active_harmonics:
                signal += np.sin(2 * np.pi * f0 * h * t_vals)
            signal /= len(active_harmonics)
            return axes.plot_line_graph(
                x_values=t_vals - t0,  # shift so window starts at 0
                y_values=signal,
                line_color=YELLOW,
                add_vertex_dots=False,
            )

        # Start with only the fundamental
        active_harmonics = [harmonics[0]]
        signal_graph = always_redraw(get_signal)

        self.play(Create(signal_graph))

        # Animate time progression and harmonic addition
        time_per_harmonic = duration / len(harmonics)
        for h in harmonics[1:]:
            self.play(
                t_tracker.animate.set_value(t_tracker.get_value() + time_per_harmonic),
                run_time=time_per_harmonic,
                rate_func=linear,
            )
            active_harmonics.append(h)

        # Final stretch with all harmonics
        remaining_time = duration - t_tracker.get_value()
        if remaining_time > 0:
            self.play(
                t_tracker.animate.set_value(duration),
                run_time=remaining_time,
                rate_func=linear,
            )

        self.wait()

if __name__ == "__main__":
    scene = ScrollingHarmonics()
    scene.render()

