import tkinter as tk

from _OLD.GUI.GUI_State import GUI_State


class GUI_ecra2(GUI_State):

    def __init__(self, baseGui):
        super().__init__(name="", BaseGUI=baseGui)
        self.active = False

        self.canvasImage = None
        self.image_index = 0

        self.frameBase = tk.Frame(
            master=baseGui.container,
            height=1000,
            width=1000,
            background="black"
        )
        self.frameBase.pack()
        self.frameBase.pack_propagate(False)

        # Label para clicar
        self.label = tk.Label(
            master=self.frameBase,
            text="Gosto desta"
        )
        self.label.place(
            x=700,
            y=700,
            anchor="center"
        )

        self.buttonRight = tk.Button(
            master=self.frameBase,
            text=">>"
        )
        self.buttonRight.place(
            x=800,
            y=700,
            anchor="center"
        )
        self.buttonLeft = tk.Button(
            master=self.frameBase,
            text=">>"
        )
        self.buttonLeft.place(
            x=600,
            y=700,
            anchor="center"
        )

    def enterGUI(self):
        super().enterGUI()
        self.executeGui()

    def exitGUI(self):
        super().exitGUI()
        self.active = False

    def executeGui(self):
        super().exitGUI()
        self.active = True
        self.frameBase.tkraise()
