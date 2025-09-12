import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use("QtAgg")  # For interactive window (needs PyQt installed)


# Parameters
f0 = 2.5
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
ax.set_xlim(0, window_width)
ax.set_ylim(-1.2, 1.2)
(line,) = ax.plot([], [], lw=2)


# Animation update function
def update(frame):
    start = frame
    end = frame + int(window_width * sample_rate)
    line.set_data(t[start:end] - t[start], signal[start:end])
    return (line,)


# Create animation
frames = len(t) - int(window_width * sample_rate)
ani = FuncAnimation(fig, update, frames=frames, interval=50, blit=True)

plt.show()


if __name__ == "__main__":
    ani.save("./media/images/scrolling_harmonics.gif", writer="pillow", fps=20)
