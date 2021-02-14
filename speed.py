import PySimpleGUIQt as cute
import threading
import time
import random
from enum import Enum

class State(Enum):
    READY = 1
    INACTIVE = 2
    PREPARING = 3
    ACTIVE = 4
state = [State.READY] # must be a mutable type
startTime = 0.0
LIGHTSPEED = 299792458 # m/s
random.seed()

cute.theme("DarkBlack")

layout = [  [cute.Text("Press the button when you're ready. The button will go dark.")],
            [cute.Text("Then, after some time, it will light up for you to click.")],
            [cute.Text("Your reaction time to click the button will be compared to the speed of light!")],
            [cute.Button("Ready", key="-BUTTON-"), cute.Quit()],
            [cute.Text("Results will appear here", key="-RES1-")],
            [cute.Text("", key="-RES2-")]]

window = cute.Window("The Speed Of Light", layout)

def startGame():
    state.pop(0)
    state.append(State.PREPARING)

while True:
    event, values = window.read(timeout=1000)
    print(event, values, state)

    if state[0] == State.PREPARING:
        # Timer has elapsed, start the challenge
        window["-BUTTON-"].update(text = "Click!", disabled = False, button_color = cute.theme_button_color())
        state.pop(0)
        state.append(State.ACTIVE)
        # start timer to count time taken
        startTime = time.perf_counter()

    if event in (cute.WIN_CLOSED, "Quit"):
        break

    if event == "-BUTTON-":
        if state[0] == State.READY:
            # User is ready
            window["-BUTTON-"].update(text = "Wait", disabled = True, button_color = ("black", "gray"))
            state.pop(0)
            state.append(State.INACTIVE)
            # start a timer to wait before changing button to "Click!"
            timeToWait = random.uniform(1, 3)
            t = threading.Timer(timeToWait, startGame)
            t.start()

        if state[0] == State.ACTIVE:
            # User clicked the button, the challenge is over

            # calculate time from when the button changed to when it was clicked
            # reset and show results
            reactionTime = time.perf_counter() - startTime
            lightDistance = (reactionTime * LIGHTSPEED)/1000

            window["-RES1-"].update("In the {0:n} seconds it took you to click the button,".format(reactionTime))
            window["-RES2-"].update("light has traveled {0:n} kilometres".format(lightDistance))
            window["-BUTTON-"].update("Ready")
            state.pop(0)
            state.append(State.READY)


window.close()