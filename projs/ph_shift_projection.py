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
        self.wait(2)

    def show_heading(self):
        heading = MathTex(r"y = \sin(x - \psi), \psi = \frac{\pi}{4}").scale(0.8)
        heading.to_edge(UP)
        self.add(heading)

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
        x_labels = [
            MathTex(r"0"),
            MathTex(r"\pi"),
            MathTex(r"2 \pi"),
            MathTex(r"3 \pi"),
            MathTex(r"4 \pi"),
        ]
       
        for i in range(len(x_labels)):
            x_labels[i].next_to(np.array([-3 + 2 * i, 0, 0]), DOWN)
            
            self.add(x_labels[i])

    def show_circle(self):
        circle = Circle(radius=1)
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
                stroke_width=2,
            ).set_color([GREY, BLACK, GREY, BLACK, GREY])
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
