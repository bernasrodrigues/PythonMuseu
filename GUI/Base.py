import glob
import os
import sys
import time
import tkinter as tk

from SoundPlayer.SoundPlayer import SoundPlayer

sys.path.append("..")
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from tkinter import font as tkfont
from PIL import Image, ImageTk

from ChoosePage import ChoosePage
from CompPage import CompPage
from ResultPage import ResultPage
from StartPage import StartPage
from PostalPage import PostalPage
from PostalPageFinal import PostalPageFinal
from Photos.CameraHandler import CameraHandler
from Photos.MontageHandler import MontageHandler
from Listener.MouseListener import MouseListener
from Settings import SettingsHandler
from Settings.SettingsHandler import settings

##########################################################################################################
# Pages to add to the list of Pages
Pages = (StartPage, ChoosePage, CompPage, ResultPage, PostalPage, PostalPageFinal)


def LoadSettings():
    currentDirectory = os.getcwd()
    parentDirectory = os.path.dirname(currentDirectory)
    pathToSettingsFromParent = os.path.join(parentDirectory, 'Settings', 'settings.txt')
    SettingsHandler.ReadSettingsFromFile(pathToSettingsFromParent)
    print(f'settings loaded: {settings["testVariable"]}\n------------')


class GUI_Base(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        LoadSettings()

        self.timer = None

        self.currentFrame = None
        self.debugMode = False
        self.language = "_PT"

        """ Load Image Data """
        self.images_intro = []

        self.degrade = tk.PhotoImage(file='Images/degrade.png')

        for image in glob.glob('../Photos/IntroImages/*'):
            pilImage = Image.open(image)
            tkImage = ImageTk.PhotoImage(pilImage)
            self.images_intro.append(tkImage)
        """"""

        self.title_font = tkfont.Font(family='Helvetica', size=20, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in Pages:  # ADD PAGES
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

            if self.debugMode:
                button = tk.Button(self, text="Go to " + F.__name__,
                                   command=lambda: self.show_frame(F.__name__))
                button.pack()

        # self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        if self.currentFrame is not None:
            self.currentFrame.ExitFrame()

        self.currentFrame = self.frames[page_name]
        self.currentFrame.EnterFrame()
        self.currentFrame.tkraise()
        self.refreshTimer(settings["pageTimeout"])

    def start_timer(self, timeoutTimer):
        self.timer = self.after(timeoutTimer * 1000, self.show_frame, "StartPage")

    def refreshTimer(self, timeoutTimer):
        if self.timer:
            self.after_cancel(self.timer)

        self.start_timer(timeoutTimer=timeoutTimer)

    def SetMontageToFirst(self):
        MontageHandler.Instance().SetMontageToFirst()

    def GetNextMontageCover(self, direction):
        MontageHandler.Instance().GetNextElement(direction)
        return self.GetMontageCover()

    def GetMontageCover(self):
        coverImage = MontageHandler.Instance().GetCurrentMontageCoverImage()
        image = ImageTk.PhotoImage(coverImage)
        return image

    def GetMontageExample(self):
        coverImage = MontageHandler.Instance().GetCurrentMontageExampleImage()
        image = ImageTk.PhotoImage(coverImage)
        return image

    ### User Image
    def CreateUserMontageImage(self, function):  # Create montage with user image
        cameraImage = CameraHandler.Instance().GetPilImage()
        montageImage = MontageHandler.Instance().CreateMontageUserImage(cameraImage, function)
        finalImage = ImageTk.PhotoImage(montageImage)

        return finalImage

    def GetUserMontageImage(self):  # Get montage with the user image

        montageImage = MontageHandler.Instance().GetUserMontageImage()
        finalImage = ImageTk.PhotoImage(montageImage)
        return finalImage

    ### Postal Image
    def CreatePostalMontageImage(self):  # Create postal with the user image
        postal = MontageHandler.Instance().CreateMontagePostalImage()
        postal = ImageTk.PhotoImage(postal)
        return postal

    def GetPostalMontageImage(self):  # Get Postal with the user image
        postal = MontageHandler.Instance().GetPostalMontageImage()
        postal = ImageTk.PhotoImage(postal)
        return postal

    def SavePostalImage(self, barcode):  # save postal image
        image = MontageHandler.Instance().GetPostalMontageImage()
        current_time = int(time.time())  # time since epoch
        time_string = str(current_time)  # Convert it to a string
        fileType = "png"

        saveFile = '{0}{1}_{2}.{3}'.format(settings["UserPostageFolder"], barcode, time_string, fileType)
        image.save(saveFile)

    def SetLang(self, lang):
        print("set language to " + lang[1:])
        self.language = lang


if __name__ == "__main__":
    # Initialize app
    app = GUI_Base()

    # Initialize the camera and start the recording process
    CameraHandler.Instance().StartRecording()

    # Initialize the montages
    MontageHandler.Instance()

    # Initialize the MouseListener
    MouseListener.Instance()
    MouseListener.Instance().AssignController(app)
    MouseListener.Instance().Start()

    # Initialize SoundPlayer
    SoundPlayer.Instance()

    # Initialize the GUI application
    app.geometry(f'{settings["windowWidth"]}x{settings["windowHeight"]}')
    # app.overrideredirect(True)                 # dont use
    app.attributes('-fullscreen', not settings["debug"])  # start in full screen borderless

    app.show_frame("StartPage")
    app.mainloop()
