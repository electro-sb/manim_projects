from manim import *

class APlusBWholeSq(Scene):
    def construct(self):
        self.camera.background_color = "#05212a"  # DARK_BLUE
        #Setup a right angle triangle with sides a, b and c
        base_length = 2
        height_length = 1
        A = ORIGIN +3*LEFT
        B = A + base_length * RIGHT
        C = A + height_length * UP
        triangle = Polygon(A, B, C, color=BLUE, fill_opacity=0.5)
        self.play(Create(triangle))
        self.wait(1)


if __name__ == "__main__":
    scene = APlusBWholeSq()
    scene.render()