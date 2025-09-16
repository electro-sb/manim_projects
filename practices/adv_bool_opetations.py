from manim import *


class BooleanOperations(Scene):
    def construct(self):
        self.camera.background_color = "#0a2126"
        math_text_color = "#f5f543"

        bool_ops_text = MarkupText("<u>Boolean Operations</u>").move_to(UP * 3.5)
        self.play(FadeIn(bool_ops_text))

        ellipse1 = Ellipse(
            width=4.0, height=5.0, fill_opacity=0.5, color=BLUE, stroke_width=10
        ).move_to(LEFT)
        e1_txt = MathTex("Set A", color=math_text_color).move_to(ellipse1.get_center())

        ellipse2 = ellipse1.copy().set_color(color=RED).move_to(RIGHT)
        e2_txt = MathTex("Set B", color=math_text_color).move_to(ellipse2.get_center())

        ellipse1.add(e1_txt)
        ellipse2.add(e2_txt)

        ellipse_group = Group(ellipse1, ellipse2).move_to(LEFT * 4)
        self.play(FadeIn(ellipse_group))

        i = Intersection(ellipse1, ellipse2, color=GREEN, fill_opacity=0.5)
        self.play(i.animate.scale(0.25).move_to(RIGHT * 3 + UP * 1.5))
        intersection_text = Text("Intersection", font_size=23, color=LIGHT_GREY).next_to(i, UP)
        intersection_math = MathTex("A \\cap B", color=math_text_color).move_to(i.get_center())
        self.play(FadeIn(intersection_text), FadeIn(intersection_math))

        u = Union(ellipse1, ellipse2, color=ORANGE, fill_opacity=0.5)
        union_text = Text("Union", font_size=23, color=LIGHT_GREY)
        self.play(u.animate.scale(0.3).next_to(i, DOWN, buff=union_text.height * 3))
        union_text.next_to(u, UP)
        union_math = MathTex("A \\cup B", color=math_text_color).move_to(u.get_center())
        self.play(FadeIn(union_text), FadeIn(union_math))

        e = Exclusion(ellipse1, ellipse2, color=YELLOW, fill_opacity=0.5)
        exclusion_text = Text("Exclusion", font_size=23, color=LIGHT_GREY)
        self.play(
            e.animate.scale(0.3).next_to(u, DOWN, buff=exclusion_text.height * 3.5)
        )
        exclusion_math = MathTex("A \\oplus B", color=math_text_color).move_to(e.get_center())
        exclusion_text.next_to(e, UP)
        self.play(FadeIn(exclusion_text), FadeIn(exclusion_math))

        d_l = Difference(ellipse1, ellipse2, color=PINK, fill_opacity=0.5)
        diff1_text = Text("Difference", font_size=23, color=LIGHT_GREY)
        self.play(
            d_l.animate.scale(0.3).next_to(u, LEFT, buff=diff1_text.height * 3.5)
        )
        diff1_text.next_to(d_l, UP)
        diff1_math = MathTex("A - B", color=math_text_color).move_to(d_l.get_center())
        self.play(FadeIn(diff1_text), FadeIn(diff1_math))

        d_2 = Difference(ellipse2, ellipse1, color=PURPLE, fill_opacity=0.5)
        diff2_text = Text("Difference", font_size=23, color=LIGHT_GREY)

        self.play(
            d_2.animate.scale(0.3).next_to(u, RIGHT, buff=diff2_text.height * 3.5)
        )
        diff2_text.next_to(d_2, UP)
        diff2_math = MathTex("B - A", color=math_text_color).move_to(d_2.get_center())
        self.play(FadeIn(diff2_text), FadeIn(diff2_math))
        self.wait(2)


if __name__ == "__main__":
    Scene= BooleanOperations()
    Scene.render()
