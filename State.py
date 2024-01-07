from StateMachine import StateMachine


class State:

    def __init__(self, name=None):
        if name is None:
            self.name = self.__class__.__name__

    def enterState(self):
        print(f'Entered State {self.name}')
        pass

    def exitState(self):
        print(f'Exited State {self.name}')
        pass

    def execute(self):
        print(f'Executing State {self.name}')
        pass
