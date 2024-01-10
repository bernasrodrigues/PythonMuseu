from States.StateEnum import StateEnum
from States.StatePhoto import StatePhoto
from States.StateWaiting import StateWaiting


class StateMachine:

    def __init__(self, name=None):
        self.name = None
        self.states = {}
        self.currentState = None

        self.name = name
        print(f'creating state machine: "{self.name}"')

        # Creating states in the state machine dictionary
        self.states = {}

        # Creating waiting state
        stateWaiting = StateWaiting(name=StateEnum.WAITING, stateMachineContext=self)
        self.states[stateWaiting.name] = stateWaiting

        # Creating photo state
        statePhoto = StatePhoto(name=StateEnum.PHOTO, stateMachineContext=self)
        self.states[statePhoto.name] = statePhoto

        # setting current state
        self.currentState = self.states[stateWaiting.name]

        print(f'Initialized State Machine: {self.name}')

    # Given the enum of the next state (equivalent to the name of the state), change the current state to the next state
    def changeState(self, nextState):
        nextState = self.states[nextState]
        print(f'----------------------------------------------------------------\n'
              f'Changing state from {self.currentState.name} to {nextState.name}')
        self.currentState.exitState()

        self.currentState = nextState

        self.currentState.enterState()
        print(f'----------------------------------------------------------------')

    def executeState(self):
        print(f'{self.name} - Executing state {self.currentState.name}')
        self.currentState.execute()
