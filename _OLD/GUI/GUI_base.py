import glob
import tkinter as tk
from PIL import Image, ImageTk

from _OLD.GUI.GUI_ecra1 import GUI_ecra1
from _OLD.GUI.GUI_ecra2 import GUI_ecra2


class GUI_base():

    def __init__(self):
        self.window = tk.Tk()
        self.window.config(bg="gray")
        # window.geometry = "2000x2000"

        self.images_intro = []
        for image in glob.glob('../Photos/IntroImages/*'):
            pilImage = Image.open(image)
            tkImage = ImageTk.PhotoImage(pilImage)
            self.images_intro.append(tkImage)

        self.container = tk.Frame()
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames_dict = {}

        self.frames = []
        self.activeGUI = None

    def initializeFrames(self):
        startGui = GUI_ecra1(self)
        self.frames.append(startGui)
        escolhaGui = GUI_ecra2(self)
        self.frames.append(escolhaGui)

        self.activeGUI = escolhaGui

    def startGUI(self):
        # self.activeGUI.enterGUI()

        self.window.after(100, self.activeGUI.enterGUI)
        self.window.mainloop()

    def changeGUI(self, nextGUI):
        print("Changing GUI frame")
        """
        nextState = self.states[nextState]
        print(f'----------------------------------------------------------------\n'
              f'Changing state from {self.currentState.name} to {nextState.name}')
        self.currentState.exitState()

        self.currentState = nextState

        self.currentState.enterState()
        print(f'----------------------------------------------------------------')
        """
        self.activeGUI.exitGUI()
        self.activeGUI = nextGUI
        self.activeGUI.enterGUI()


"""
# Base frame
frameBase = tk.Frame(
    master=window,
    height=1000,
    width=1000,
    background="gray65"
)
frameBase.pack()
frameBase.pack_propagate(False)

# Image canvas
canvasImage = tk.Canvas(
    frameBase,
    # width=1000,
    # height=1000
)
canvasImage.pack(
    fill="both",
    expand=True,
    # padx=(10, 10),
    # pady=(10,10),
    anchor="center"
)
canvasImage.create_image(0, 0, image=images_intro[image_intro_index], anchor="nw")

# Label para clicar
label = tk.Label(
    master=canvasImage,
    text="Toque no ecra para dar inicio à selfie"
)
label.place(
    x=500,
    y=500,
    anchor="center"
)


def ImageCarrousel():
    print("AAAAAAA")
    global image_intro_index

    if image_intro_index == len(images_intro) - 1:
        canvasImage.create_image(0, 0, image=images_intro[image_intro_index], anchor="nw")
        image_intro_index = 0
    else:
        canvasImage.create_image(0, 0, image=images_intro[image_intro_index], anchor="nw")
        image_intro_index += 1

    window.after(2000, ImageCarrousel)


ImageCarrousel()
frameBase
window.mainloop()

"""
