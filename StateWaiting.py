import threading

from State import State


class StateWaiting(State):

    def __init__(self, name):
        super().__init__(name=name)

        self.condition_set_by_user = False
        self.condition_lock = threading.Lock()
        self.condition_event = threading.Event()

    def enterState(self):
        super().enterState()

    def exitState(self):
        super().exitState()

    def execute(self):
        userCondition_thread = threading.Thread(target=self.waitForUserCondition)
        userInput_thread = threading.Thread(target=self.setUserInput)
        userCondition_thread.start()
        userInput_thread.start()

        userInput_thread.join()
        userCondition_thread.join()

    # TODO
    # Temporary implementation of waiting for user input
    def waitForUserCondition(self):
        print(f'Waiting for user condition...')
        self.condition_event.wait()

        print(f'User condition is set! \n Moving into new State')


    # TODO
    # Temporary Implementation of the user condition to move unto the next state (maybe button press in the future idk)
    def setUserInput(self):
        while True:
            user_input = input("Enter 'yes' to set the condition: ")
            if user_input.lower() == 'yes':
                # with self.condition_lock:
                #    self.condition_set_by_user = True
                self.condition_event.set()
                return
            else:
                print("AAAAAAA")
