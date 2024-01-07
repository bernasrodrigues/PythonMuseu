class StateMachine:

    def __init__(self, name=None, states=None, currentState=None):
        self.name = None
        self.states = {}
        self.currentState = None

        # name handling
        if name is None:
            name = "State Machine"
        self.name = name
        print(f'creating state machine "{self.name}"')

        # adding list of states
        if states is None:
            states = {}
        self.state = states

        # setting current state
        self.currentState = currentState

        print(f'Initialized State Machine {self.name}')


    def changeState(self, currentState, nextState):
        currentState.exitState()
        print(f'Changing state from {currentState} to {nextState}')
        nextState.enterState()

    def executeState(self):
        print(f'Executing state {self.currentState}')
        self.currentState.execute()
