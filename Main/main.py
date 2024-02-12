import time

from GUI.GUI_base import GUI_base
from Photos import PhotoHandler


def main():
    # State Machine
    # state_Machine = StateMachine(name="State Machine")
    # state_Machine.executeState()

    gui = GUI_base()
    gui.initializeFrames()
    gui.startGUI()


if __name__ == '__main__':
    main()
