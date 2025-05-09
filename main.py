import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from rotatingArrow import RotatingArrow
from matplotlib.widgets import RadioButtons, TextBox, Button


# Initialize arrows and traces
arrows = []
num_arrows = 2
y_limits1 = [-3.5, 3.5]
x_limits1 = [-3.5,3.5]
y_limits2 = [-3.5, 3.5]
x_limits2 = [0,1]
simulationSpan = 2 * 360
trace1_x = []
trace1_y = []
trace2_x = []
trace2_y = []

# Set up the figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5),gridspec_kw={'width_ratios': [2, 2]})

ax1.set_position([0.1, 0.1, 0.35, 0.6])  # [left, bottom, width, height]
ax2.set_position([0.55, 0.1, 0.35, 0.6])  # [left, bottom, width, height]

ax1.set_xlim(x_limits1)
ax1.set_ylim(y_limits1)
ax1.set_title(f"Vector sum {num_arrows}")
ax1.grid(True)
ax2.set_xlim(x_limits2)
ax2.set_ylim(y_limits2)
ax2.set_title('Sinousoids sum')
ax2.grid(True)

chosen_function = 'square wave'  # Default function

functions = {
    'square wave': {
        'n': lambda x: 2 * x + 1,
        'length': lambda n: 4 / (np.pi * n),
        'frequency': lambda n: n,
    },
    'sawtooth wave': {
        'n': lambda x: x + 1,
        'length': lambda n: 2 / n,
        'frequency': lambda n: n,
    },
    'tilted wave': {
        'n': lambda x: x + 1,
        'length': lambda n: 4 / (n ** 2 * np.pi),
        'frequency': lambda n: n,
    },  
    'triangle wave': {
        'n': lambda x: 2 * x + 1,
        'length': lambda n: (-1)**((n-1)/2)/n**2*8/np.pi**2,
        'frequency': lambda n: n,
    },
}

def initialize_arrows(function):
    global arrows, lengths, frequencies
    arrows.clear()
    lengths = np.zeros(num_arrows)
    frequencies = np.zeros(num_arrows)
    for i in range(num_arrows):
        n = function['n'](i)
        lengths[i] = function['length'](n)
        frequencies[i] = function['frequency'](n) 

        
        arrows.append(RotatingArrow(ax1, 'b-', length=lengths[i], frequency=frequencies[i]))


initialize_arrows(functions[chosen_function])

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


# Update the text label whenever the number of arrows changes
def update_num_arrows_text():
    ax1.set_title(f"Vector sum {num_arrows}")

# Add buttons
def increment_arrows(event):
    global num_arrows, ani
    num_arrows += 1
    initialize_arrows(functions[chosen_function])
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
        initialize_arrows(functions[chosen_function])
        # Clear previous traces
        trace1_x.clear()
        trace1_y.clear()
        trace2_x.clear()
        trace2_y.clear()
        ani.event_source.stop()  # Stop the current animation
        ani = FuncAnimation(fig, update, frames=np.arange(0, simulationSpan, 1), init_func=init, blit=True, interval=20)
        ani.event_source.start()  # Restart the animation
        update_num_arrows_text()  # Update the displayed number of arrows

def update_chosen_function(label):
    global chosen_function, ani
    chosen_function = label
    initialize_arrows(functions[chosen_function])
    # Clear previous traces
    trace1_x.clear()
    trace1_y.clear()
    trace2_x.clear()
    trace2_y.clear()
    trace1.set_data([], [])
    trace2.set_data([], [])
    ani.event_source.stop()  # Stop the current animation
    ani = FuncAnimation(fig, update, frames=np.arange(0, simulationSpan, 1), init_func=init, blit=True, interval=20)
    ani.event_source.start()  # Restart the animation

# Function to update y_limits1
def update_y_limits1(text):
    global y_limits1
    try:
        y_limits1 = list(map(float, text.split(',')))  # Parse input as a list of two floats
        ax1.set_ylim(y_limits1)  # Update the y-limits of ax1
        plt.draw()  # Redraw the plot
    except ValueError:
        print("Invalid input for y_limits1. Please enter two comma-separated numbers.")

# Function to update x_limits1
def update_x_limits1(text):
    global x_limits1
    try:
        x_limits1 = list(map(float, text.split(',')))  # Parse input as a list of two floats
        ax1.set_xlim(x_limits1)  # Update the x-limits of ax1
        plt.draw()  # Redraw the plot
    except ValueError:
        print("Invalid input for x_limits1. Please enter two comma-separated numbers.")

# Add input fields for y_limits1 and x_limits1
ax_y_limits = plt.axes([0.2, 0.9, 0.2, 0.05])  # Position for y_limits1 input field
ax_x_limits = plt.axes([0.2, 0.8, 0.2, 0.05])  # Position for x_limits1 input field
ax_radio = plt.axes([0.75, 0.8, 0.15, 0.2], facecolor='lightgoldenrodyellow')  # Position for the radio buttons
ax_inc = plt.axes([0.92, 0.6, 0.075, 0.075])  # Position for increment button
ax_dec = plt.axes([0.92, 0.4, 0.075, 0.075])  # Position for decrement button


radio = RadioButtons(ax_radio, list(functions.keys()))
btn_inc = Button(ax_inc, '+')
btn_dec = Button(ax_dec, '-')
text_y_limits = TextBox(ax_y_limits, 'Y Limits (ax1):', initial=f"{y_limits1[0]},{y_limits1[1]}")
text_x_limits = TextBox(ax_x_limits, 'X Limits (ax1):', initial=f"{x_limits1[0]},{x_limits1[1]}")

radio.on_clicked(update_chosen_function)
btn_inc.on_clicked(increment_arrows)
btn_dec.on_clicked(decrement_arrows)
text_y_limits.on_submit(update_y_limits1)  # Connect the input field to the update function
text_x_limits.on_submit(update_x_limits1)  # Connect the input field to the update function


plt.show()