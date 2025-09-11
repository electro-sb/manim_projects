from manim import *

class CircleScene(Scene):
    def construct(self):
        circle = Circle()  # Create a circle
        circle.set_stroke(GREEN, width=4)  # Set the outline color and width
        circle.set_fill(ORANGE, opacity=0.5)  # Set the color and transparency
        self.play(Create(circle))  # Show the circle on screen
        self.wait(1)  # Wait for a second

if __name__ == "__main__":
    scene = CircleScene()
    scene.render()