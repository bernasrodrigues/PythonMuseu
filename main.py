# This is a sample Python script.
from State import State
from StateMachine import StateMachine
from StateWaiting import StateWaiting


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    # States
    stateWaiting = StateWaiting(name="Waiting State")
    stateA = State(name="StateA")
    stateB = State(name="StateB")
    stateC = State(name="StateC")

    # State Machine
    state_Machine = StateMachine(name=StateMachine, states=None, currentState=stateWaiting)

    state_Machine.executeState()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
