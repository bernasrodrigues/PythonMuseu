import tkinter as tk

from _OLD.GUI.GUI_State import GUI_State


class GUI_ecra1(GUI_State):

    def __init__(self, baseGui):
        super().__init__(name="", BaseGUI=baseGui)
        self.active = False

        self.canvasImage = None
        self.image_index = 0

        self.frameBase = tk.Frame(
            master=baseGui.container,
            height=1000,
            width=1000,
            background="gray65"
        )
        self.frameBase.pack()
        self.frameBase.pack_propagate(False)

        # Image canvas
        self.canvasImage = tk.Canvas(
            self.frameBase,
            # width=1000,
            # height=1000
        )
        self.canvasImage.pack(
            fill="both",
            expand=True,
            # padx=(10, 10),
            # pady=(10,10),
            anchor="center"
        )
        self.canvasImage.create_image(0, 0, image=baseGui.images_intro[self.image_index], anchor="nw")
        self.canvasImage.bind("<Button-1>", lambda e: self.BaseGUI.changeGUI(self.BaseGUI.frames[1]))

        # Label para clicar
        self.label = tk.Label(
            master=self.frameBase,
            text="Toque no ecra para dar inicio à selfie"
        )
        self.label.place(
            x=500,
            y=500,
            anchor="center"
        )


    def ImageCarrousel(self):

        if self.active:
            if self.image_index == len(self.BaseGUI.images_intro) - 1:
                self.canvasImage.create_image(0, 0, image=self.BaseGUI.images_intro[self.image_index], anchor="nw")
                self.image_index = 0
            else:
                self.canvasImage.create_image(0, 0, image=self.BaseGUI.images_intro[self.image_index], anchor="nw")
                self.image_index += 1

            self.canvasImage.after(2000, self.ImageCarrousel)

    def start(self):
        self.ImageCarrousel()

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
