import glob
import tkinter as tk
from tkinter import font as tkfont  # python 3

from PIL import Image, ImageTk

from GUI2.GUI_ChoosePage import ChoosePage
from GUI2.GUI_CompPage import CompPage
from GUI2.GUI_ResultPage import ResultPage
from GUI2.GUI_StartPage import StartPage
from Photos.CameraHandler import CameraHandler
from Photos.MontageHandler import MontageHandler


class GUI_Base(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.currentFrame = None
        self.debugMode = False
        """
        Load Image Data
        """
        self.images_intro = []
        for image in glob.glob('../Photos/IntroImages/*'):
            pilImage = Image.open(image)
            tkImage = ImageTk.PhotoImage(pilImage)
            self.images_intro.append(tkImage)

        self.images_choice = []
        for image in glob.glob('../Photos/ChoiceImages/*'):
            pilImage = Image.open(image)
            tkImage = ImageTk.PhotoImage(pilImage)
            self.images_choice.append(tkImage)
        """
        
        """

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ChoosePage, CompPage, ResultPage):  # ADD PAGES
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

            debugButtons = []
            if self.debugMode:
                button = tk.Button(self, text="Go to " + F.__name__,
                                   command=lambda: self.show_frame(F.__name__))
                button.pack()

        self.show_frame("StartPage")

    def show_frame(self, page_name):

        '''Show a frame for the given page name'''
        if self.currentFrame is not None:
            self.currentFrame.ExitFrame()

        self.currentFrame = self.frames[page_name]
        self.currentFrame.EnterFrame()
        self.currentFrame.tkraise()

    def SetMontageToFirst(self):
        MontageHandler.Instance().SetMontageToFirst()

    def GetNextMontageCover(self, direction):
        MontageHandler.Instance().GetNextElement(direction)
        return self.GetMontageCover()

    def GetMontageCover(self):

        coverImage = MontageHandler.Instance().GetCurrentMontageCoverImage()
        image = ImageTk.PhotoImage(coverImage)

        return image
        # return MontageHandler.Instance().GetCurrentMontageCoverImage()

    def CreateFinalImage(self):
        cameraImage = CameraHandler.Instance().GetPilImage()
        montageImage = MontageHandler.Instance().CreateMontageFinalImage(cameraImage)
        finalImage = ImageTk.PhotoImage(montageImage)

        return finalImage

    def GetFinalImage(self):

        montageImage = MontageHandler.Instance().GetFinalImage()
        finalImage = ImageTk.PhotoImage(montageImage)
        return finalImage


if __name__ == "__main__":
    CameraHandler.Instance().StartRecording()
    MontageHandler.Instance()
    app = GUI_Base()
    app.mainloop()

'''
im = Image.open(pathToImage)
ph = ImageTk.PhotoImage(im)
'''
