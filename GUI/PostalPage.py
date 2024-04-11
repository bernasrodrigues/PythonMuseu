import tkinter as tk  # python 3

import PIL
import keyboard
from PIL import ImageTk

from Settings.SettingsHandler import settings


class PostalPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #########################################
        self.image_index = 0
        self.active = False
        self.barCode = ""

        ### Canvas ###
        # Canvas
        self.canvas = tk.Canvas(
            self,
            width=1080,
            height=1980,
            background='black'

        )
        self.canvas.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER
        )

        # Final image presentation initially set to none
        self.canvas_image = self.canvas.create_image(settings["postal_Image_X"],
                                                     settings["postal_Image_Y"],
                                                     anchor=tk.CENTER,
                                                     image=None)

        self.canvas_text = self.canvas.create_text(settings["postal_Title_X"],
                                                   settings["postal_Title_Y"],
                                                   text=settings["postal_Title_Text_PT"],
                                                   fill=settings["postal_Title_Fill"],
                                                   font=settings["postal_Title_Font"])

        '''
        # degrade
        self.canvas_degrade = self.canvas.create_image(1080 / 2, 1980 / 2,
                                                       anchor=tk.CENTER,
                                                       image=self.controller.degrade)
        '''

        #self.canvas.bind("<Button-1>", lambda e: self.controller.show_frame("PostalPageFinal"))

    def EnterFrame(self):
        self.active = True
        self.barCode = ""  # reset barcode
        print("Showing Postal Image")

        # create postal , resize and set the image to postal
        postal = self.controller.CreatePostalMontageImage()
        postal = self.ResizePostal(postal, settings["postal_Image_resize_X"], settings["postal_Image_resize_Y"])
        #postal = self.ResizePostal(postal, 500, 500)

        self.ConfigureImage(postal)  # on enter create postal image

        keyboard.on_press(self.on_barcode_scan)  # start listening to keyboard
        #self.canvas.after(10000, self.MoveToNextPage)           # move to next page

    def ResizePostal(self, postal, x, y):
        postal = ImageTk.getimage(postal)  # convert to pil
        size = (x, y)
        postal = postal.resize(size)  # resize it
        postal = ImageTk.PhotoImage(postal)  # convert to photo image
        return postal

    def ConfigureImage(self, image):
        self.canvas.image = image  # <- Prevent garbage collection from deleting the image (tkinter is stupid)
        self.canvas.itemconfig(self.canvas_image, image=image)

    def on_barcode_scan(self, event):
        if self.active:
            if event.name == 'enter':
                print("Enter key pressed")
                print("Final barcode:", self.barCode)
                self.controller.SavePostalImage(self.barCode)

                self.barCode = ""  # reset barcode (just to be safe)

                self.controller.show_frame("PostalPageFinal")

            else:
                self.barCode += event.name
                # Handle barcode scanning
                print("Barcode scanned:", self.barCode)

    # automatically move to next page if not clicked
    def MoveToNextPage(self):
        if self.active:
            self.controller.show_frame("PostalPageFinal")

    def ExitFrame(self):
        keyboard.unhook_all()  # stop listening to keyboard
        self.active = False
