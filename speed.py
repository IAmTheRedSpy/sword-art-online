import PySimpleGUIQt as cute
import threading
import time
from enum import Enum

class State(Enum):
    READY = 1
    INACTIVE = 2
    PREPARING = 3
    ACTIVE = 4
state = [State.READY] # must be a mutable type
startTime = 0.0
LIGHTSPEED = 299792458 # m/s

cute.theme("DarkBlack")

layout = [  [cute.Text("Press the button when you're ready")],
            [cute.Text("The button will go dark then after some time it will light up for you to click")],
            [cute.Text("Afterwards, your reaction time will be compared to the speed of light!")],
            [cute.Button("Ready", key="-BUTTON-"), cute.Quit()],
            [cute.Text("Results will appear here", key="-RES-")]]

window = cute.Window("The Speed Of Light", layout)

def startGame():
    state.pop(0)
    state.append(State.PREPARING)

while True:
    event, values = window.read(timeout=1000)
    print(event, values, state)

    if state[0] == State.PREPARING:
        # Timer has elapsed, start the challenge
        window["-BUTTON-"].update(text = "Click!", disabled = False)
        state.pop(0)
        state.append(State.ACTIVE)
        # start timer to count time taken
        startTime = time.perf_counter()

    if event in (cute.WIN_CLOSED, "Quit"):
        break

    if event == "-BUTTON-":
        if state[0] == State.READY:
            # User is ready
            window["-BUTTON-"].update(text = "Wait", disabled = True)
            state.pop(0)
            state.append(State.INACTIVE)
            # start a timer to wait before changing button to "Click!"
            t = threading.Timer(2.0, startGame)
            t.start()

        if state[0] == State.ACTIVE:
            # User clicked the button, the challenge is over

            # calculate time from when the button changed to when it was clicked
            # reset and show results
            reactionTime = time.perf_counter() - startTime
            lightDistance = (reactionTime * LIGHTSPEED)/1000

            window["-RES-"].update("In the {0:n} seconds it took you to click the button, light has traveled {1:n} kilometres".format(reactionTime, lightDistance))
            window["-BUTTON-"].update("Ready")
            state.pop(0)
            state.append(State.READY)


window.close()