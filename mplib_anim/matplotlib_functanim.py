import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use("QtAgg")  # For interactive window (needs PyQt installed)
import time


# Parameters
f0 = 0.5 #2.5
harmonics = [1, 3, 5, 7]
duration = 20
sample_rate = 200
window_width = 4  # seconds visible at a time

# Time vector for the whole signal
t = np.linspace(0, duration, int(sample_rate * duration))
signal = np.zeros_like(t)
for h in harmonics:
    signal += np.sin(2 * np.pi * f0 * h * t)
signal /= len(harmonics)

# Set up figure
fig, ax = plt.subplots()
xdata, ydata = [], []
ax.set_xlim(0, window_width)
ax.set_ylim(-1.2, 1.2)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Amplitude')
ax.set_title(f'Scrolling Harmonic Signal{f" (f0={f0} Hz)"} harmonics={harmonics}')
(line,) = ax.plot([], [], lw=2)


# Animation update function
def update(frame):
    start = frame
    end = frame + int(window_width * sample_rate)
    line.set_data(t[start:end] - t[start], signal[start:end])
    return (line,)


# Create animation
# frames = len(t) - int(window_width * sample_rate)
# ani = FuncAnimation(fig, update, frames=frames, interval=50, blit=True)


# Time blimited frame updates
def init():
    line.set_data([], [])
    return (line,)


# Update function (scrolling window)
def update(frame_idx):
    start = frame_idx
    end = frame_idx + int(window_width * sample_rate)
    line.set_data(t[start:end] - t[start], signal[start:end])
    return (line,)


# Frame generator for time-limited animation
start_time = time.perf_counter()


def frame_gen():
    frame_idx = 0
    while time.perf_counter() - start_time < duration:
        yield frame_idx
        frame_idx += 1


ani = FuncAnimation(fig, update, frames=frame_gen, init_func=init, blit=True)

# plt.show()


if __name__ == "__main__":
    # ani.save("./media/images/scrolling_harmonics.gif", writer="pillow", fps=20)
    ani.save("./media/videos/1080p60/mpl_harmonics.mp4", writer="ffmpeg", fps=20)  # To save as mp4
