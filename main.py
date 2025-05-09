import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from rotatingArrow import RotatingArrow



# Initialize arrows and traces
arrows = []
num_arrows = 2
y_limits1 = [-3, 3]
x_limits1 = [-3,3]
y_limits2 = [-3, 3]
x_limits2 = [0,1]
simulationSpan = 2 * 360
trace1_x = []
trace1_y = []
trace2_x = []
trace2_y = []

# Set up the figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
ax1.set_xlim(x_limits1)
ax1.set_ylim(y_limits1)
ax1.set_title('Vector sum')
ax1.grid(True)
ax2.set_xlim(x_limits2)
ax2.set_ylim(y_limits2)
ax2.set_title('Sinousoids sum')
ax2.grid(True)


def initialize_arrows():
    global arrows, lengths, frequencies
    arrows.clear()
    lengths = np.zeros(num_arrows)
    frequencies = np.zeros(num_arrows)
    for i in range(num_arrows):
        n = 2 * i + 1
        lengths[i] = 4 / (np.pi * n)
        frequencies[i] = n
        arrows.append(RotatingArrow(ax1, 'b-', length=lengths[i], frequency=frequencies[i]))

initialize_arrows()

trace1, = ax1.plot([], [], 'g-', lw=1)
trace2, = ax2.plot([], [], 'g-', lw=1)

def init():
    for arrow in arrows:
        arrow.reset()
    trace1.set_data([], [])
    trace2.set_data([], [])
    return [arrow.arrow for arrow in arrows] + [trace1, trace2]

def update(frame):
    global trace1_x, trace1_y, trace2_x, trace2_y
    x_start, y_start = 0, 0
    for arrow in arrows:
        x_start, y_start = arrow.update(frame, x_start=x_start, y_start=y_start)
    trace1_x.append(x_start)
    trace1_y.append(y_start)
    trace2_x.append(frame / simulationSpan)
    trace2_y.append(y_start)
    trace1.set_data(trace1_x, trace1_y)
    trace2.set_data(trace2_x, trace2_y)
    return [arrow.arrow for arrow in arrows] + [trace1, trace2]

ani = FuncAnimation(fig, update, frames=np.arange(0, simulationSpan, 1), init_func=init, blit=True, interval=20)

# Add a text label to display the number of arrows
num_arrows_text = ax1.text(-2.5, 2.5, f"Terms: {num_arrows}", fontsize=12, color='black')

# Update the text label whenever the number of arrows changes
def update_num_arrows_text():
    num_arrows_text.set_text(f"Terms: {num_arrows}")

# Add buttons
def increment_arrows(event):
    global num_arrows, ani
    num_arrows += 1
    initialize_arrows()
    # Clear previous traces
    trace1_x.clear()
    trace1_y.clear()
    trace2_x.clear()
    trace2_y.clear()
    ani.event_source.stop()  # Stop the current animation
    ani = FuncAnimation(fig, update, frames=np.arange(0, simulationSpan, 1), init_func=init, blit=True, interval=20)
    ani.event_source.start()  # Restart the animation
    update_num_arrows_text()  # Update the displayed number of arrows

def decrement_arrows(event):
    global num_arrows, ani
    if num_arrows > 1:
        num_arrows -= 1
        initialize_arrows()
        # Clear previous traces
        trace1_x.clear()
        trace1_y.clear()
        trace2_x.clear()
        trace2_y.clear()
        ani.event_source.stop()  # Stop the current animation
        ani = FuncAnimation(fig, update, frames=np.arange(0, simulationSpan, 1), init_func=init, blit=True, interval=20)
        ani.event_source.start()  # Restart the animation
        update_num_arrows_text()  # Update the displayed number of arrows

ax_inc = plt.axes([0.92, 0.6, 0.075, 0.075])  # Position for increment button
ax_dec = plt.axes([0.92, 0.4, 0.075, 0.075])  # Position for decrement button
btn_inc = Button(ax_inc, '+')
btn_dec = Button(ax_dec, '-')
btn_inc.on_clicked(increment_arrows)
btn_dec.on_clicked(decrement_arrows)

plt.show()