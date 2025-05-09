import numpy as np
import matplotlib.pyplot as plt

class RotatingArrow:
    def __init__(self, ax, color, length=1, frequency=1):
        self.ax = ax
        self.color = color
        self.length = length
        self.frequency = frequency
        self.arrow, = ax.plot([], [], color, lw=2)
        self.x_start = 0
        self.y_start = 0

    def update(self, frame, x_start=0, y_start=0):
        self.x_start = x_start
        self.y_start = y_start
        angle = np.radians(self.frequency * frame)
        x_end = self.x_start + self.length * np.cos(angle)
        y_end = self.y_start + self.length * np.sin(angle)
        self.arrow.set_data([self.x_start, x_end], [self.y_start, y_end])
        return x_end, y_end

    def reset(self):
        self.arrow.set_data([], [])