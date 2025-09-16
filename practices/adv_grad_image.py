from manim import *


class GradientImageFromArray(Scene):
    def construct(self):
        self.camera.background_color = "#0f1e22"
        n = 256
        imageArray = np.uint8([[i * 256 / n for i in range(0, n)] for _ in range(0, n)])
        image = ImageMobject(imageArray).scale(2)
        image.background_rectangle = SurroundingRectangle(image, color=GREEN)
        self.add(image, image.background_rectangle)


if __name__ == "__main__":
    scene = GradientImageFromArray()
    scene.render()