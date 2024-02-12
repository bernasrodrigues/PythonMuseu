class GUI_State:

    def __init__(self, name=None, BaseGUI=None):
        self.name = name
        self.BaseGUI = BaseGUI

        print(f'Initialized GUI {self.name}')

    def enterGUI(self):
        print(f'Entered GUI {self.name}')
        pass

    def exitGUI(self):
        print(f'Exited GUI {self.name}')
        pass

    def executeGUI(self):
        print(f'{self.name} Executing GUI ')
        pass
