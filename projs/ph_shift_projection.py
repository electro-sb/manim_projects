from manim import *

class DynamicDashedLine(VGroup):
    def __init__(self, start_fn, end_fn, dash_length=0.2, gap_length=0.1, **kwargs):
        super().__init__(**kwargs)
        self.start_fn = start_fn  # functions returning points
        self.end_fn = end_fn
        self.dash_length = dash_length
        self.gap_length = gap_length
        self.kwargs = kwargs
        self.update_line()

    def update_line(self):
        # Clear existing submobjects
        self.submobjects = []

        start = np.array(self.start_fn())
        end = np.array(self.end_fn())
        vec = end - start
        length = np.linalg.norm(vec)
        if length == 0:
            return
        direction = vec / length

        pos = 0
        while pos < length:
            dash_end = min(pos + self.dash_length, length)
            seg = Line(
                start + pos * direction, start + dash_end * direction, **self.kwargs
            )
            self.add(seg)
            pos += self.dash_length + self.gap_length

    def update(self, dt=0):
        self.update_line()
        return self


class ShiftSineProjection(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.origin_point = np.array([-3, 0, 0])
        self.circle_origin = np.array([-4, 0, 0])
        self.curve_start = np.array([-3, 0, 0])

    def construct(self):
        self.show_axis()
        self.show_circle()
        self.show_heading()
        self.move_dot_and_draw_curve()
        self.wait()

    def show_heading(self):
        heading = MarkupText("<u>Phase Shifted Sine Wave Projection</u>").scale(0.8)
        heading.to_edge(UP)
        footer = MathTex(r"y = \sin(\omega t - \psi), \psi = \frac{\pi}{4}").scale(0.8)
        footer.set_color(YELLOW)
        footer.next_to(heading, DOWN)
        self.add(heading, footer)

    def show_axis(self):
        x_start = np.array([-6, 0, 0])
        x_end = np.array([6, 0, 0])

        y_start = np.array([-3, -2, 0])
        y_end = np.array([-3, 2, 0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

    def add_x_labels(self):
        # Labels at multiples of π
        x_labels = [
            MathTex(r"\dot"),
            MathTex(r"\frac{\pi}{2}"),
            MathTex(r"\pi"),
            MathTex(r"\frac{3\pi}{2}"),
            MathTex(r"2\pi"),
            MathTex(r"\frac{4\pi}{2}"),
        ]
        # Group to hold ticks
        ticks = VGroup()
        x_axis_offset = -3.0   # y-axis is at x = -3
        step = np.pi/2 
        mul_fac = 0.05
        # Add labels and ticks
        for i, label in enumerate(x_labels):
            x_pos = x_axis_offset + i * step   # 0, π, 2π, 3π, 4π
            pos = np.array([x_pos, 0, 0])
            label.next_to(pos, DOWN)
            if mul_fac == 0.1:
                mul_fac= 0.05 
            elif mul_fac== 0.05:
                mul_fac= 0.1
            tick = Line(
                pos + mul_fac * DOWN, pos + mul_fac * UP, color=WHITE, stroke_width=2
            )
            ticks.add(tick)
            self.add(label.scale(0.5))

        # Add all ticks at once
        self.add(ticks)
        # X axis name
        x_name = MathTex(r"\omega t \rightarrow").next_to(np.array([6, 0, 0]), DOWN*2)
        y_name = MathTex(r"\uparrow y").next_to(np.array([-3, 2, 0]), LEFT)
        # Y Ticks and labels
        yt_tick = Line(np.array([-3, 1, 0]) + 0.1 * RIGHT, np.array([-3, 1, 0]) + 0.1 * LEFT, color=WHITE, stroke_width=2)
        yb_tick = Line(np.array([-3, -1, 0]) + 0.1 * RIGHT, np.array([-3, -1, 0]) + 0.1 * LEFT, color=WHITE, stroke_width=2)
        y_peak = MathTex(r"1").next_to(np.array([-3, 1, 0]), RIGHT).scale(0.5)
        y_zero = MathTex(r"(0,0)").next_to(np.array([-3, 0, 0]), DOWN).scale(0.5)
        y_least = MathTex(r"-1").next_to(np.array([-3, -1, 0]), RIGHT).scale(0.5)
        self.add(y_peak,y_zero, y_least, yt_tick, yb_tick)
        self.add(y_name, x_name)

    def show_circle(self):
        circle = Circle(radius=1)
        circle.set_color(GREEN)
        circle.move_to(self.circle_origin)
        self.add(circle)
        self.circle = circle

    def move_dot_and_draw_curve(self):
        orbit = self.circle
        psi = PI/4
        rate = 0.25
        x_max = 6  # right end of axis

        # a(t) is the "x" parameter along the sine curve
        self.a = ValueTracker(0.0)

        # Dot starts at angle (a - psi)
        dot = Dot(radius=0.08, color=YELLOW)
        dot.move_to(orbit.point_at_angle(self.a.get_value() - psi))

        def update_dot(mob, dt):
            # Predict next x position
            next_a = self.a.get_value() + rate * TAU * dt
            next_x = self.curve_start[0] + next_a

            if next_x >= x_max:
                # Clamp to final position and stop
                self.a.set_value(x_max - self.curve_start[0])
                mob.move_to(orbit.point_at_angle(self.a.get_value() - psi))
                mob.remove_updater(update_dot)
                return

            # Otherwise keep moving
            self.a.increment_value(rate * TAU * dt)
            mob.move_to(orbit.point_at_angle(self.a.get_value() - psi))

        dot.add_updater(update_dot)

        # Radial line
        line_to_dot = always_redraw(
            lambda: Line(self.circle_origin, dot.get_center(), color=BLUE)
        )

        # proj_horizontal = DynamicDashedLine(
        #     start_fn=lambda: dot.get_center(),
        #     end_fn=lambda: np.array(
        #         [self.curve_start[0] + self.a.get_value(), dot.get_center()[1], 0]
        #     ),
        #     dash_length=0.2,
        #     gap_length=0.1,
        #     color=GREY_E,
        #     stroke_width=0.5,
        # )

        proj_horizontal = always_redraw(
            lambda: Line(
                start=dot.get_center(),
                end=np.array(
                    [self.curve_start[0] + self.a.get_value(), dot.get_center()[1], 0]
                ),
                stroke_width=0.25,
                stroke_opacity=0.7,
                stroke_color=ORANGE,
                color=ORANGE,
            )
        )

        # Vertical projection
        dot_to_curve_line = always_redraw(
            lambda: Line(
                dot.get_center(),
                np.array([
                    self.curve_start[0] + self.a.get_value(),
                    dot.get_center()[1],
                    0
                ]),
                color=YELLOW_A,
                stroke_width=2,
            )
        )

        # Initialize curve at (0, sin(-ψ))
        start_x = self.curve_start[0]
        start_y = np.sin(-psi)
        self.curve = VGroup(Line([start_x, start_y, 0], [start_x, start_y, 0], color=YELLOW_D))

        def get_curve():
            last_line = self.curve[-1]
            x = start_x + self.a.get_value()
            y = dot.get_center()[1]
            if x > last_line.get_end()[0] and x <= x_max:
                self.curve.add(Line(last_line.get_end(), np.array([x, y, 0]), color=YELLOW_D))
            return self.curve

        sine_curve_line = always_redraw(get_curve)

        self.add(orbit, dot, line_to_dot, proj_horizontal, dot_to_curve_line, sine_curve_line)
        self.wait(8.5)
        dot.remove_updater(update_dot)


if __name__ == "__main__":
    scene = ShiftSineProjection()
    scene.render()
