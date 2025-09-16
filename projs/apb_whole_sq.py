from manim import *

class APlusBWholeSq(Scene):
    def construct(self):
        self.camera.background_color = "#05212a"  # DARK_BLUE
        a = 3
        b = 2
        # Setup a square with side a+b
        apb_outer = Square(side_length=(a+b), color=BLUE)
        apb_outer.set_fill(BLUE, opacity=0.5)
        # Label the sides
        top_txt = MathTex("a+b").next_to(apb_outer, UP)
        left_txt = MathTex("a+b").next_to(apb_outer, LEFT).rotate(PI/2)
        apb_label= MathTex("(a+b)^2").move_to(apb_outer.get_center())

        lgroup = VGroup(apb_outer, top_txt, left_txt, apb_label)
        self.play(Create(lgroup),
                  run_time=2)
        self.play(
            lgroup.animate.shift(LEFT * 3),
            run_time=2
        )

        # print equals
        equals = MathTex("=").next_to(lgroup, RIGHT)
        self.play(Write(equals), run_time=2)

        # Create the inner squares and rectangles
        a_square = Square(side_length=a, color=YELLOW).set_fill(YELLOW, opacity=0.5)
        b_square = Square(side_length=b, color=GREEN).set_fill(GREEN, opacity=0.5)
        ab_rect1 = Rectangle(width=a, height=b, color=RED).set_fill(RED, opacity=0.5)
        ab_rect2 = Rectangle(width=a, height=b, color=RED).set_fill(RED, opacity=0.5)
        ab_rect2.rotate(PI/2)
        # a_square.right_to(equals, RIGHT, buff=1)
        ab_rect2.next_to(a_square, RIGHT, buff=0)
        b_square.next_to(ab_rect2, RIGHT, buff=0)
        ab_rect1.next_to(a_square, DOWN, buff=0)
        b_square.next_to(ab_rect1, RIGHT, buff=0)

        # label the top and the left sides
        a_txt_top = MathTex("a").next_to(a_square, UP)
        a_txt_left = MathTex("a").next_to(a_square, LEFT).rotate(PI/2)
        b_txt_top = MathTex("b").next_to(ab_rect2, UP)
        b_txt_right = MathTex("b").next_to(ab_rect1, LEFT).rotate(PI/2)
        asq_label = MathTex("a^2").move_to(a_square.get_center())
        bsq_label = MathTex("b^2").move_to(b_square.get_center())
        ab1_label = MathTex("ab").move_to(ab_rect1.get_center())
        ab2_label = MathTex("ab").move_to(ab_rect2.get_center())
        # Group them
        rgroup = VGroup(a_square, b_square, ab_rect1, ab_rect2,
                             a_txt_top, a_txt_left, b_txt_top, b_txt_right,
                             asq_label, bsq_label, ab1_label, ab2_label)
        # shift to the right of equals
        rgroup.next_to(equals, RIGHT, buff=1)
        self.play(Create(rgroup), run_time=2)
        self.wait(1)

        # Final equation
        final_eq = MathTex(
            r"(a+b)^2", r"=", r"{{a^2}}", r"+", r"{{2ab}}", r"+", r"{{b^2}}"
        ).scale(0.9)

        final_eq.next_to(VGroup(lgroup, rgroup).get_top(), UP, buff= -0.1)

        # targets
        a2b_target = final_eq[0]
        a2_target = final_eq[2]
        ab_target = final_eq[4]
        b2_target = final_eq[6]

        a2b_target.set_color(BLUE)
        a2_target.set_color(YELLOW)
        ab_target.set_color(RED)
        b2_target.set_color(GREEN)

        # copies
        a2b_copy = apb_label.copy()
        a2_copy = asq_label.copy()
        ab1_copy = ab1_label.copy()
        ab2_copy = ab2_label.copy()
        b2_copy = bsq_label.copy()

        # Animation
        self.play(
            ReplacementTransform(a2b_copy, a2b_target),
            ReplacementTransform(a2_copy, a2_target),
            ReplacementTransform(ab1_copy, ab_target),
            ReplacementTransform(ab2_copy, ab_target),
            ReplacementTransform(b2_copy, b2_target),
            Write(final_eq[1]),  # "="
            Write(final_eq[3]),  # "+"
            Write(final_eq[5]),  # "+"
            run_time=3
        )
        self.wait(2)


if __name__ == "__main__":
    scene = APlusBWholeSq()
    scene.render()
