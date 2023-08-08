import struct
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# set up the plot
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.set_thetamin(0)
ax.set_thetamax(180)

# initialize an empty line plot for the polygon
line, = ax.plot([], [], 'r-', alpha=0.5)  # Red line connecting the points


# function to initialize the plot
def init():
    line.set_data([], [])  # Initialize the line plot with empty data
    return line,


# function to update the plot
def update(data):
    dists, angles = data
    max_normal_val = 1700  # argument,  1200
    for i in range(len(dists)):  # remove for
        if dists[i] > max_normal_val:
            dists[i] = dists[i - 1]

    # update the line plot with the polygon
    line.set_data(np.append(angles, angles[0]), np.append(dists, dists[0]))  # Close the polygon

    ax.set_rlim(0, 1700)

    return line,


# function to read data from 'lidar.raw' in a loop
def read_lidar_data():
    angles = np.linspace(0.0, np.pi, 721)
    while True:
        with open('lidar2.raw', 'rb') as f:  # read all lidar files in loop
            buf = f.read(2 + 8 + 1 + 721 * 2 + 1 + 4 + 2)
            dists_time = struct.unpack_from('>721H', buf, 11)
            dists = np.asarray(dists_time)
            yield (dists, angles)


# create the animation
ani = FuncAnimation(fig, update, frames=read_lidar_data, init_func=init, blit=True, interval=100)

# show the plot
plt.show()
