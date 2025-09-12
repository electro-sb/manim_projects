from manim import *
import numpy as np


class ScrollingHarmonicsWithHeading(Scene):
    def construct(self):
        # Parameters
        f0 = 2.5  # Hz
        harmonics = [1, 3, 5, 7]
        duration = 20
        window_width = 4
        sample_rate = 200

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

        # Time tracker
        t_tracker = ValueTracker(0)

        # Active harmonics list
        active_harmonics = [harmonics[0]]

        # Signal generator
        def get_signal():
            t0 = t_tracker.get_value()
            t_vals = np.linspace(t0, t0 + window_width, int(sample_rate * window_width))
            signal = np.zeros_like(t_vals)
            for h in active_harmonics:
                signal += np.sin(2 * np.pi * f0 * h * t_vals)
            signal /= len(active_harmonics)
            return axes.plot_line_graph(
                x_values=t_vals - t0,
                y_values=signal,
                line_color=YELLOW,
                add_vertex_dots=False,
            )

        # Heading generator
        heading = always_redraw(
            lambda: MathTex(
                r"\text{Harmonics: }"
                + ", ".join(
                    [
                        f"{h}^{{\\text{{th}}}}" if h != 1 else "1^{\\text{st}}"
                        for h in active_harmonics
                    ]
                )
                + rf"\ \ (f_0 = {f0}\,\text{{Hz}})"
            )
            .scale(0.7)
            .to_edge(UP)
        )

        # Add heading and signal
        signal_graph = always_redraw(get_signal)
        self.play(FadeIn(heading), Create(signal_graph))

        # Animate time + harmonic additions
        time_per_harmonic = duration / len(harmonics)
        for h in harmonics[1:]:
            self.play(
                t_tracker.animate.set_value(t_tracker.get_value() + time_per_harmonic),
                run_time=time_per_harmonic,
                rate_func=linear,
            )
            active_harmonics.append(h)

        # Final stretch
        remaining_time = duration - t_tracker.get_value()
        if remaining_time > 0:
            self.play(
                t_tracker.animate.set_value(duration),
                run_time=remaining_time,
                rate_func=linear,
            )

        self.wait()


if __name__ == "__main__":
    scene = ScrollingHarmonicsWithHeading()
    scene.render()