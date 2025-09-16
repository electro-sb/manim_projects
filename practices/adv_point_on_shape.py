from manim import *


class PointMovingOnShapes(Scene):
    def construct(self):
        circle = Circle(radius=1, color=BLUE)
        dot = Dot()
        dot2 = dot.copy().shift(RIGHT)
        dot2.set_color(GREEN)
        dot3 = dot.copy().shift(RIGHT)
        dot3.set_color(YELLOW)
        self.add(dot)

        line = Line([3, 0, 0], [5, 0, 0])
        self.add(line)

        self.play(GrowFromCenter(circle))
        self.play(Transform(dot, dot2))
        self.play(MoveAlongPath(dot, circle), run_time=2, rate_func=linear)
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
        self.play(Rotating(dot, about_point=[3, 0, 0]), run_time=1.5)
        self.play(Transform(dot, dot3))
        self.play(MoveAlongPath(dot3, line), run_time=2, rate_func=linear)
        self.wait()


if __name__ == "__main__":
    Scene = PointMovingOnShapes()
    Scene.render()
