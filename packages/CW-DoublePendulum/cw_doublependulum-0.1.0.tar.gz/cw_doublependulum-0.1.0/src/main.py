import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
import time
import csv

# Initial parameters (all can be modified with sliders)
l1 = 1.0
l2 = 1.0
m1 = 1.0
m2 = 1.0
g = 9.81
dt = 0.02

# Initial conditions: [theta1, omega1, theta2, omega2]
state = np.array([np.pi / 2, 0, np.pi / 2, 0], dtype=float)

# Control flags
animationRunning = True
collectingData = False

collectedData = []

def derivs(state, l1, l2, m1, m2):
    theta1, omega1, theta2, omega2 = state
    delta = theta2 - theta1

    denom1 = (m1 + m2) * l1 - m2 * l1 * np.cos(delta)**2
    denom2 = (l2 / l1) * denom1

    domega1 = (m2 * l1 * omega1**2 * np.sin(delta) * np.cos(delta) +
           m2 * g * np.sin(theta2) * np.cos(delta) +
           m2 * l2 * omega2**2 * np.sin(delta) -
           (m1 + m2) * g * np.sin(theta1)) / denom1

    domega2 = (-m2 * l2 * omega2**2 * np.sin(delta) * np.cos(delta) +
           (m1 + m2) * g * np.sin(theta1) * np.cos(delta) -
           (m1 + m2) * l1 * omega1**2 * np.sin(delta) -
           (m1 + m2) * g * np.sin(theta2)) / denom2

    return np.array([omega1, domega1, omega2, domega2])

def step():
    global state
    k1 = derivs(state, l1, l2, m1, m2)
    k2 = derivs(state + 0.5 * dt * k1, l1, l2, m1, m2)
    k3 = derivs(state + 0.5 * dt * k2, l1, l2, m1, m2)
    k4 = derivs(state + dt * k3, l1, l2, m1, m2)
    state += (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

def getPos():
    theta1, omega1, theta2, omega2 = state
    x1 = l1 * np.sin(theta1)
    y1 = -l1 * np.cos(theta1)
    x2 = x1 + l2 * np.sin(theta2)
    y2 = y1 - l2 * np.cos(theta2)
    return x1, y1, x2, y2, theta1, omega1, theta2, omega2

def updatePlotLimits():
    # Calculate the range based on the diagonal extent of both pendulums
    # Add 20% margin
    maxRange = (l1 + l2) * 1.2
    ax.set_xlim(-maxRange, maxRange)
    ax.set_ylim(-maxRange, maxRange)
    fig.canvas.draw_idle()

# Function to convert mass to marker size
def massToSize(mass):
    return 3 + 5 * (mass ** 0.7)

# Make large figure for buttons and whatnot
fig = plt.figure(figsize=(12, 8))
# Adjust the main plot area to make room for UI elements
plt.subplots_adjust(left=0.2, right=0.8, bottom=0.2)
ax = plt.subplot(111)
ax.set_aspect('equal')
updatePlotLimits()
ax.plot(0, 0, 'ko')  # Center point/pivot
ax.set_title('Double Pendulum Simulation')

# Pendulum components
line, = ax.plot([], [], '-', lw=2, color='black')
mass1, = ax.plot([], [], 'bo', markersize=massToSize(m1))
mass2, = ax.plot([], [], 'ro', markersize=massToSize(m2))

# Trail lines
trailLength = 100
trailSegments1 = []
trailSegments2 = []
trailCmap1 = plt.get_cmap('winter') # these don't really have any gradient for some reason, idc anymore
trailCmap2 = plt.get_cmap('autumn')
trail1 = ax.add_collection(LineCollection([], linewidths=2, cmap=trailCmap1, alpha=0.6))
trail2 = ax.add_collection(LineCollection([], linewidths=2, cmap=trailCmap2, alpha=0.6))

# Trace flags
showTrace1 = True
showTrace2 = True

def init():
    line.set_data([], [])
    mass1.set_data([], [])
    mass2.set_data([], [])
    trail1.set_segments([])
    trail2.set_segments([])
    return line, mass1, mass2, trail1, trail2

def update(frame):
    global collectedData
    
    if animationRunning:
        step()
    
    x1, y1, x2, y2, theta1, omega1, theta2, omega2 = getPos()
    
    # Collect data and setup keys
    if collectingData:
        timestamp = time.time()
        collectedData.append({
            'time': timestamp,
            'theta1': theta1, 
            'omega1': omega1, 
            'theta2': theta2, 
            'omega2': omega2,
            'x1': x1, 
            'y1': y1, 
            'x2': x2, 
            'y2': y2,
            'l1': l1,
            'l2': l2,
            'm1': m1,
            'm2': m2,
            'g': g,
            'dt': dt
        })
    
    # Update pendulum position
    line.set_data([0, x1, x2], [0, y1, y2])
    mass1.set_data([x1], [y1])
    mass2.set_data([x2], [y2])
    
    # Update trail if animation is running
    if animationRunning:
        if len(trailSegments1) > 0:
            prevX1, prevY1 = trailSegments1[-1][-1]
            prevX2, prevY2 = trailSegments2[-1][-1]
            
            trailSegments1.append([[prevX1, prevY1], [x1, y1]])
            trailSegments2.append([[prevX2, prevY2], [x2, y2]])
        else:
            trailSegments1.append([[x1, y1], [x1, y1]])
            trailSegments2.append([[x2, y2], [x2, y2]])
        
        # Limit trail length
        if len(trailSegments1) > trailLength:
            trailSegments1.pop(0)
            trailSegments2.pop(0)
    
    # Update trail if enabled
    if showTrace1 and len(trailSegments1) > 0:
        n = len(trailSegments1)
        alphas = np.linspace(0.0, 1.0, n)
        trail1.set_segments(trailSegments1)
        trail1.set_array(alphas)
    else:
        trail1.set_segments([])
    
    if showTrace2 and len(trailSegments2) > 0:
        n = len(trailSegments2)
        alphas = np.linspace(0.0, 1.0, n)
        trail2.set_segments(trailSegments2)
        trail2.set_array(alphas)
    else:
        trail2.set_segments([])
    
    return line, mass1, mass2, trail1, trail2

ani = FuncAnimation(fig, update, init_func=init, blit=True, interval=20)

# -------------------- LAYOUT ARRANGEMENT --------------------
axcolor = 'lightgoldenrodyellow'

# ---- SLIDERS (RIGHT SIDE) ----
sliderWidth = 0.15
sliderHeight = 0.03
sliderLeft = 0.82
sliderGap = 0.05

# Create slider axes on the right side
axM1 = plt.axes([sliderLeft, 0.7, sliderWidth, sliderHeight], facecolor=axcolor)
axM2 = plt.axes([sliderLeft, 0.7 - sliderGap, sliderWidth, sliderHeight], facecolor=axcolor)
axL1 = plt.axes([sliderLeft, 0.7 - 2*sliderGap, sliderWidth, sliderHeight], facecolor=axcolor)
axL2 = plt.axes([sliderLeft, 0.7 - 3*sliderGap, sliderWidth, sliderHeight], facecolor=axcolor)
axG  = plt.axes([sliderLeft, 0.7 - 4*sliderGap, sliderWidth, sliderHeight], facecolor=axcolor)
axDt = plt.axes([sliderLeft, 0.7 - 5*sliderGap, sliderWidth, sliderHeight], facecolor=axcolor)

# Create sliders
sliderM1 = Slider(axM1, 'Mass 1', 0.1, 5.0, valinit=m1)
sliderM2 = Slider(axM2, 'Mass 2', 0.1, 5.0, valinit=m2)
sliderL1 = Slider(axL1, 'Length 1', 0.1, 2.0, valinit=l1)
sliderL2 = Slider(axL2, 'Length 2', 0.1, 2.0, valinit=l2)
sliderG  = Slider(axG, 'Gravity', 0.1, 20.0, valinit=g)
sliderDt = Slider(axDt, 'Time Step', 0.005, 0.05, valinit=dt)

# ---- BUTTONS (LEFT SIDE) ----
buttonWidth = 0.15
buttonHeight = 0.05
buttonLeft = 0.02
buttonGap = 0.06

# Add checkbox buttons for trails
rax = plt.axes([buttonLeft, 0.7, buttonWidth, 0.1], facecolor=axcolor)
check = CheckButtons(
    rax, ['Trail 1', 'Trail 2'], 
    [showTrace1, showTrace2]
)

# Add buttons
resetAx = plt.axes([buttonLeft, 0.6, buttonWidth, buttonHeight], facecolor=axcolor)
pauseAx = plt.axes([buttonLeft, 0.6 - buttonGap, buttonWidth, buttonHeight], facecolor=axcolor)
collectAx = plt.axes([buttonLeft, 0.6 - 2*buttonGap, buttonWidth, buttonHeight], facecolor=axcolor)

resetButton = plt.Button(resetAx, 'Reset', color=axcolor)
pauseButton = plt.Button(pauseAx, 'Pause', color=axcolor)
collectButton = plt.Button(collectAx, 'Collect Data', color=axcolor)

# -------------------- CALLBACKS -------------------- be careful >:(
def updateSliders(val):
    global m1, m2, l1, l2, g, dt
    if not collectingData:  # Only allow changes when not collecting data
        m1 = sliderM1.val
        m2 = sliderM2.val
        l1 = sliderL1.val
        l2 = sliderL2.val
        g = sliderG.val
        dt = sliderDt.val
        
        # Update mass marker sizes based on new mass values
        mass1.set_markersize(massToSize(m1))
        mass2.set_markersize(massToSize(m2))
        updatePlotLimits()
        
        # Clear trails when parameters change
        trailSegments1.clear()
        trailSegments2.clear()
        trail1.set_segments([])
        trail2.set_segments([])

sliderM1.on_changed(updateSliders)
sliderM2.on_changed(updateSliders)
sliderL1.on_changed(updateSliders)
sliderL2.on_changed(updateSliders)
sliderG.on_changed(updateSliders)
sliderDt.on_changed(updateSliders)

def toggleTrace(label):
    global showTrace1, showTrace2
    if label == 'Trail 1':
        showTrace1 = not showTrace1
        if not showTrace1:
            trail1.set_segments([])
    elif label == 'Trail 2':
        showTrace2 = not showTrace2
        if not showTrace2:
            trail2.set_segments([])

check.on_clicked(toggleTrace)

def reset(event):
    global state, trailSegments1, trailSegments2
    if not collectingData:  # Only reset when not collecting data dummy
        state = np.array([np.pi / 2, 0, np.pi / 2, 0], dtype=float)
        trailSegments1.clear()
        trailSegments2.clear()
        trail1.set_segments([])
        trail2.set_segments([])

resetButton.on_clicked(reset)

def toggleAnimation(event):
    global animationRunning
    animationRunning = not animationRunning
    pauseButton.label.set_text('Play' if not animationRunning else 'Pause')

pauseButton.on_clicked(toggleAnimation)

def toggleDataCollection(event):
    global collectingData, collectedData
    
    collectingData = not collectingData
    
    if collectingData:
        collectButton.label.set_text('Stop Collecting')
        collectedData = []  # Clear previous data
        
        # Disable sliders to ensure good data | might change and allow different stuff, but i see weird behavior idk
        sliderM1.active = False
        sliderM2.active = False
        sliderL1.active = False
        sliderL2.active = False
        sliderG.active = False
        sliderDt.active = False
        
        # Change slider colors to show they have been imprisoned, how sad it doesn't work
        axM1.set_facecolor('red')
        axM2.set_facecolor('red')
        axL1.set_facecolor('red')
        axL2.set_facecolor('red')
        axG.set_facecolor('red')
        axDt.set_facecolor('red')
        
    else:
        # Save data
        collectButton.label.set_text('Collect Data')
        
        # Reenable
        sliderM1.active = True
        sliderM2.active = True
        sliderL1.active = True
        sliderL2.active = True
        sliderG.active = True
        sliderDt.active = True
        
        # Restore da colors
        axM1.set_facecolor(axcolor)
        axM2.set_facecolor(axcolor)
        axL1.set_facecolor(axcolor)
        axL2.set_facecolor(axcolor)
        axG.set_facecolor(axcolor)
        axDt.set_facecolor(axcolor)
        
        # Save data to file
        if collectedData:
            filename = f"pendulum_data_{int(time.time())}.csv"
            saveDataToFile(filename)
            plt.figtext(0.5, 0.01, f"Data saved to {filename}", ha="center", bbox={"facecolor":"green", "alpha":0.5, "pad":5})
            fig.canvas.draw_idle()

collectButton.on_clicked(toggleDataCollection)

def saveDataToFile(filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['time', 'theta1', 'omega1', 'theta2', 'omega2', 'x1', 'y1', 'x2', 'y2', 'l1', 'l2', 'm1', 'm2', 'g', 'dt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for dataPoint in collectedData:
            writer.writerow(dataPoint)

# Super duper text box that tells you super duper controls idk what im saying anymore
infoText = """Controls:
- Use sliders to adjust parameters
- Toggle trails with checkboxes
- Pause/Play the simulation
- Reset to initial state
- Collect data for analysis
"""
# Make da box
fig.text(0.02, 0.2, infoText, fontsize=9, bbox=dict(facecolor=axcolor, alpha=0.5))

plt.show()