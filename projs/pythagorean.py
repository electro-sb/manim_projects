from manim import *

import math


class PythagorasProof(Scene):
    def construct(self):
        self.camera.background_color = "#05212a"  # DARK_BLUE
        # Parameters
        a = 3
        b = 2
        tri_color = BLUE

        def edge_labels(square, corner_pair, label1, label2, buff=0.1):
            p1 = square.get_corner(corner_pair[0])
            p2 = square.get_corner(corner_pair[1])
            mid = (p1 + p2) / 2
            mid1 = (p1 + mid) / 2
            mid2 = (mid + p2) / 2

            # Determine orientation from coordinates
            if abs(p1[1] - p2[1]) < 1e-6:  # y-coords equal → horizontal edge
                direction = UP
            else:  # vertical edge
                direction = LEFT

            return (
                MathTex(label1).scale(0.7).next_to(mid1, direction, buff=buff),
                MathTex(label2).scale(0.7).next_to(mid2, direction, buff=buff)
            )

        # Step 1: Base triangle
        A = ORIGIN
        B = A + a * RIGHT
        C = A + b * UP

        #for C position
        hyp_mid_dot = Dot(
            point=(B + C) / 2,
            radius=0.05,
            color=WHITE,
            fill_opacity=0  # fully transparent
        )

      
        triangle = Polygon(A, B, C, color=WHITE, fill_color=tri_color, fill_opacity=0.6)
        a_label = MathTex("b").next_to(Line(A, C), LEFT)
        b_label = MathTex("a").next_to(Line(A, B), DOWN)
        c_label = MathTex("c").next_to(hyp_mid_dot, UR)

        group1 = VGroup(triangle, hyp_mid_dot, a_label, b_label, c_label)

        self.play(Create(group1))
        self.wait(2)

        # # Step 2: Move to top-left
        # shift_vec = UP * (a + b) / 2 + LEFT * (a + b) / 2
        # self.play(group1.animate.shift(shift_vec))
        # #self.wait(1)
        self.play(FadeOut(group1), scale=0.5)
        #self.wait(1)

        # Outer square side length
        outer_side = a + b

        # Base triangle in bottom-left corner
        A = ORIGIN
        B = A + a * RIGHT
        C = A + b * UP
        triangle = Polygon(A, B, C, color=WHITE, fill_color=tri_color, fill_opacity=0.6)
        # a_label = MathTex("a").next_to(Line(A, C), LEFT)
        # b_label = MathTex("b").next_to(Line(A, B), DOWN)

        # Shift so right angle is at bottom-left of outer square
        triangle.shift(LEFT * outer_side/2 + DOWN * outer_side/2)

        # Center of the big square
        center_point = ORIGIN

        # Create the other three triangles by rotating around the center of the big square
        triangles_1 = VGroup(
            triangle,
            triangle.copy().rotate(PI/2, about_point=center_point),
            triangle.copy().rotate(PI, about_point=center_point),
            triangle.copy().rotate(3*PI/2, about_point=center_point)
        )

        self.play(FadeIn(triangles_1))
        #self.wait()

        # Inner c^2 square
        c = (a**2 + b**2)**0.5
        c_square = Square(side_length=c, color=WHITE).move_to(center_point)
        c_square.rotate(math.atan(a/b))  # Rotate to align with triangles
        c_square.set_fill(WHITE, opacity=1.0)
        self.play(Create(c_square))
        text_c2 = MathTex("c^2", color=RED).move_to(center_point)
        self.play(Write(text_c2))
        self.wait()

        # create a group with triangle and square
        group2 = VGroup(triangles_1, c_square, text_c2)
        top_a_left, top_b_left = edge_labels(group2, (UL, UR), "b", "a")
        left_b_left, left_a_left = edge_labels(group2, (UL, DL), "a", "b")
        group2.add(top_a_left, top_b_left, left_b_left, left_a_left)

        shift_group2 = LEFT * 4
        self.play(group2.animate.shift(shift_group2))
        self.wait(2)

        # Equate areas
        equals = MathTex("=").move_to(ORIGIN)
        self.play(Write(equals))

        # tri_colors = [GREEN, YELLOW, PINK, ORANGE]

        A = ORIGIN
        B = A + a * RIGHT
        C = A + b * UP
        base_triangle = Polygon(A, B, C, color=WHITE, fill_opacity=0.8)

        # Shift so right angle is at bottom-left of outer square
        base_triangle.shift(LEFT * outer_side/2 + DOWN * outer_side/2)

        # Create 4 triangles rotated around the center
        # triangles = VGroup()
        # for i, color in enumerate(tri_colors):
        #     tri = base_triangle.copy().set_fill(color)
        #     tri.rotate(i * PI/2, about_point=center_point)
        #     triangles.add(tri)

        # Create a² square (bottom-left)
        a_square = Square(side_length=a, color=WHITE).set_fill(WHITE, opacity=1.0)
        a_square.move_to(center_point + LEFT * (b/2) + DOWN * (b/2))

        # Create b² square (top-right)
        b_square = Square(side_length=b, color=WHITE).set_fill(WHITE, opacity=1.0)
        b_square.move_to(center_point + RIGHT * (a/2) + UP * (a/2))

        # Labels
        a_label = MathTex("a^2", color=BLUE).move_to(a_square)
        b_label = MathTex("b^2", color=GREEN).move_to(b_square)

        # Outer square outline
        outer_square = Square(side_length=outer_side, color=WHITE).move_to(center_point)
        outer_square.set_fill(color=tri_color, opacity=0.6)

        group3 = VGroup(outer_square, a_square, b_square, a_label, b_label)
        top_a_left, top_b_left = edge_labels(group3, (UL, UR), "a", "b")
        left_b_left, left_a_left = edge_labels(group3, (UL, DL), "b", "a")
        group3.add(top_a_left, top_b_left, left_b_left, left_a_left)
        shift_group3 = RIGHT * 4
        group3.shift(shift_group3)
        self.play(FadeIn(group3))
        self.wait(2)

        # --- Equation target layout ---
        equation = MathTex(r"c^2", "=", r"a^2", "+", r"b^2").scale(1.2)
        equation.next_to(VGroup(group2, group3).get_top(), UP, buff=0.5)

        # Map diagram labels to equation parts
        c2_target = equation[0]
        a2_target = equation[2]
        b2_target = equation[4]

        #set colors
        c2_target.set_color(RED)
        a2_target.set_color(BLUE)
        b2_target.set_color(GREEN)

        # Duplicate diagram labels for animation
        c2_copy = text_c2.copy()
        a2_copy = a_label.copy()
        b2_copy = b_label.copy()

        # Animate collection into equation
        self.play(
            ReplacementTransform(c2_copy, c2_target),
            ReplacementTransform(a2_copy, a2_target),
            ReplacementTransform(b2_copy, b2_target),
            Write(equation[1]),  # "="
            Write(equation[3]),  # "+"
        )

        self.wait(2)


if __name__ == "__main__":
    scene = PythagorasProof()
    scene.render()
