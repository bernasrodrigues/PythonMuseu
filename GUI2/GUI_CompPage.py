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

    def EnterFrame(self):
        self.active = True
        self.ShowImage()

    def ShowImage(self):
        if self.active:
            webcam_image = CameraHandler.Instance().get_current_image()
            self.Image.photo_image = webcam_image
            self.Image.configure(image=webcam_image, anchor="nw")
            self.Image.after(10, self.ShowImage)

    def ExitFrame(self):
        self.active = False
