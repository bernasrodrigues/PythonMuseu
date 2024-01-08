class State:

    def __init__(self, name=None, stateMachineContext=None):
        self.name = name
        self.stateMachineContext = stateMachineContext

        print(f'Initialized state {self.name}')

    def enterState(self):
        print(f'Entered State {self.name}')
        pass

    def exitState(self):
        print(f'Exited State {self.name}')
        pass

    def execute(self):
        print(f'{self.name} Executing State ')
        pass
