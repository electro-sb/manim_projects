from manim import *



class TransformEx(Scene):
    def construct(self):
        self.camera.background_color = "#05212a"  # DARK_BLUE
        m1 = Square().set_color(RED)
        m2 = Rectangle().set_color(BLUE).rotate(PI / 4).scale(1.5)
        self.play(Transform(m1, m2))

if __name__ == "__main__":
    scene = TransformEx()
    scene.render()
