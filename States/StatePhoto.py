import threading
from States.State import State


class StatePhoto(State):

    def __init__(self, name, stateMachineContext):
        super().__init__(name=name, stateMachineContext=stateMachineContext)

        self.montageList = []

    def enterState(self):
        super().enterState()
        self.execute()

    def exitState(self):
        super().exitState()

    def execute(self):
        super().execute()
