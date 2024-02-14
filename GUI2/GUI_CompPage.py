import tkinter as tk  # python 3
from time import sleep

from Photos.CameraHandler import CameraHandler


class CompPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #########################################
        self.image_index = 0
        self.active = False

        self.Image = tk.Label(
            self,
            width=1000,
            height=1000,
            # image=controller.images_choice[0]
        )
        self.Image.pack(
            fill="both",
            expand=True,
            # padx=(10, 10),
            # pady=(10,10),
            anchor="center",
        )
        self.Image.bind("<Button-1>", lambda e: self.controller.show_frame("ChoosePage"))

    def EnterFrame(self):
        self.active = True
        self.ShowImage()

    def ShowImage(self):
        if self.active:
            webcam_image = self.controller.CreateFinalImage()

            self.ConfigureImage(webcam_image)
            self.Image.after(100, self.ShowImage)

    def CreateImage(self):
        image = self.controller.CreateFinalImage()
        self.ConfigureImage(image)

    def ConfigureImage(self, image):
        self.Image.configure(image=image)
        self.Image.image = image  # <- Prevent garbage collection from deleting the image (tkinter is stupid)

    def ExitFrame(self):
        self.active = False
