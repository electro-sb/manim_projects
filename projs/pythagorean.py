from manim import *


class PythagorasVisual(Scene):
    def construct(self):
        self.camera.background_color = "#05212a"  # DARK_BLUE
        # Parameters
        a = 3
        b = 2
        color_triangle = BLUE
        highlight_color = WHITE

        # Points for the base triangle
        A = ORIGIN
        B = A + a * RIGHT
        C = A + b * UP

        # Triangle
        tri = Polygon(A, B, C, color=WHITE, fill_color=color_triangle, fill_opacity=0.6)
        a_label = MathTex("a").next_to(Line(A, C), LEFT)
        b_label = MathTex("b").next_to(Line(A, B), DOWN)

        # Step 1: Show triangle
        self.play(Create(tri), Write(a_label), Write(b_label))
        self.wait()

        # Step 2: Move to top-left
        self.play(
            tri.animate.shift(UP * 2 + LEFT * 3),
            a_label.animate.shift(UP * 2 + LEFT * 3),
            b_label.animate.shift(UP * 2 + LEFT * 3),
        )
        self.wait()

        # Step 3: Duplicate 4 triangles to form (a+b)² square
        tri_copies = VGroup(
            tri.copy(),
            tri.copy().rotate(PI / 2, about_point=A),
            tri.copy().rotate(PI, about_point=A),
            tri.copy().rotate(3 * PI / 2, about_point=A),
        )
        square_group = VGroup(*tri_copies).move_to(ORIGIN)
        self.play(FadeOut(tri, a_label, b_label), FadeIn(square_group))
        self.wait()

        # Inner c² square
        c = (a**2 + b**2) ** 0.5
        c_square = Square(side_length=c, color=WHITE).move_to(ORIGIN)
        self.play(Create(c_square))
        self.wait()

        # Step 4: Highlight c²
        self.play(c_square.animate.set_fill(highlight_color, opacity=0.5))
        self.wait()

        # Step 5: Duplicate (a+b)² square and move original to right
        square_copy = square_group.copy()
        self.play(
            square_group.animate.shift(LEFT * 4), FadeIn(square_copy.shift(RIGHT * 4))
        )
        self.wait()

        # Step 6: Rearrange triangles to form a² and b²
        # For simplicity, we’ll just create the a² and b² squares
        a_square = Square(side_length=a, color=WHITE).shift(LEFT * 4 + UP * (a / 2))
        b_square = Square(side_length=b, color=WHITE).shift(LEFT * 4 + DOWN * (b / 2))

        self.play(Create(a_square), Create(b_square))
        self.wait()

        # Step 7: Highlight a² and b²
        self.play(
            a_square.animate.set_fill(highlight_color, opacity=0.5),
            b_square.animate.set_fill(highlight_color, opacity=0.5),
        )
        self.wait()

        # Step 8: Show equation
        equation = MathTex("c^2 = a^2 + b^2").scale(1.5).shift(DOWN * 3)
        self.play(Write(equation))
        self.wait()

if __name__ == "__main__":
    scene = PythagorasVisual()
    scene.render()