from matplotlib.animation import FuncAnimation
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt


class WrappedFuncAnimation:
    def __init__(
        self,
        func,
        duration=30,
        window_width=5,
        sample_rate=30,
        base_path="./media/videos/1080p60/",
    ):
        self.func = np.vectorize(func)
        self.duration = duration
        self.window_width = window_width
        self.sample_rate = sample_rate
        self.total_frames = int(self.duration * self.sample_rate)
        self.t = np.linspace(0, self.duration, self.total_frames)
        self.signal = self.func(self.t)
        self.fig, self.ax, self.line = None, None, None
        self.base_path = base_path

    def create_figure(self):
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, self.window_width)
        self.ax.set_ylim(-1.2, 1.2)
        self.ax.set_xlabel("Time [s]")
        self.ax.set_ylabel("Amplitude")
        self.ax.set_title(f"{self.func.__name__} Signal Animation")
        (self.line,) = self.ax.plot([], [], lw=2)
        return self.fig, self.ax

    def _frame_initialized(self):
        self.line.set_data([], [])
        return (self.line,)

    def _frame_updated(self, frame_idx):
        start = frame_idx
        end = frame_idx + int(self.window_width * self.sample_rate)
        self.line.set_data(self.t[start:end] - self.t[start], self.signal[start:end])
        return (self.line,)

    def _frame_gen(self):
        for frame_idx in tqdm(range(self.total_frames), desc="Animating"):
            yield frame_idx

    def _make_animation(self):
        if self.fig is None:
            self.create_figure()
        return FuncAnimation(
            self.fig,
            self._frame_updated,
            frames=self._frame_gen(),
            init_func=self._frame_initialized,
            blit=True,
            cache_frame_data=False,
        )

    def save_mp4(self):
        ani = self._make_animation()
        ani.save(
            f"{self.base_path}{self.func.__name__}_animation.mp4", fps=self.sample_rate
        )

    def show(self):
        ani = self._make_animation()
        plt.show()


if __name__ == "__main__":

    def harmonic_function_135(t, hz=0.5):
        return (np.sin(2 * np.pi * hz * t)
                + 0.5 * np.sin(2 * np.pi * 3 * hz * t)
                + 0.25 * np.sin(2 * np.pi * 5 * hz * t))

    wrapped_anim = WrappedFuncAnimation(
        func=harmonic_function_135, duration=10, window_width=5, sample_rate=30
    )
    wrapped_anim.save_mp4()
    #wrapped_anim.show()
