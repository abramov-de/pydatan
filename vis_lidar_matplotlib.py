import struct
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot(111, polar=True)

# assuming the streaming data is 1D
line, = ax.plot([], [], lw=2)

ax.set_xlim(500, 600)  # assuming the x range is known
ax.set_ylim(-1, 1)  # adjust y range according to your data
ax.set_thetamin(0)
ax.set_thetamax(180)
ax.set_rlim(1000)


# generator function to simulate incoming stream data
def data_gen():
    with open('lidar.raw', 'rb') as f:
        while buf := f.read(2 + 8 + 1 + 721 * 2 + 1 + 4 + 2):
            dists_time = struct.unpack_from('>721H', buf, 11)
            dists = np.asarray(dists_time)
            yield dists


def init():
    line.set_data([], [])
    return line,


def update(data):
    angles = np.arange(0.0, 180.0, 721 / 180)
    dists = data
    for i in range(min(len(dists), len(angles))):
        line.set_data(np.append(line.get_xdata(), dists[i]),
                      np.append(line.get_ydata(), angles[i]))

    return line,


ani = animation.FuncAnimation(fig, update, frames=data_gen, init_func=init, blit=True)

plt.show()
