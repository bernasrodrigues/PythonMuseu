import tkinter as tk  # python 3

from PIL import Image, ImageTk

from Settings.SettingsHandler import settings


class PostalPageFinal(tk.Frame):

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
        self.canvas_image = self.canvas.create_image(settings["postal_Final_Image_X"],
                                                     settings["postal_Final_Image_Y"],
                                                     anchor=tk.CENTER,
                                                     image=None)

        self.canvas_text = self.canvas.create_text(settings["postal_Final_Title_X"],
                                                   settings["postal_Final_Title_Y"],
                                                   text=settings["postal_Final_Title_Text_PT"],
                                                   fill=settings["postal_Final_Title_Fill"],
                                                   font=settings["postal_Final_Title_Font"],
                                                   anchor="w")

        self.canvas_text_subtitle = self.canvas.create_text(settings["postal_Final_Subtitle_X"],
                                                            settings["postal_Final_Subtitle_Y"],
                                                            text=settings["postal_Final_Subtitle_Text_PT"],
                                                            fill=settings["postal_Final_Subtitle_Fill"],
                                                            font=settings["postal_Final_Subtitle_Font"],
                                                            anchor="w")

        # self.canvas.bind("<Button-1>", lambda e: self.controller.show_frame("StartPage"))

    def EnterFrame(self):
        self.active = True
        self.ConfigureImage(self.controller.GetPostalMontageImage())
        print("Showing Postal Final Image")

        postal = self.controller.CreatePostalMontageImage()
        postal = self.ResizeAnglePostal(postal,
                                        x=settings["postal_Final_Image_resize_X"],
                                        y=settings["postal_Final_Image_resize_Y"],
                                        angle=settings["postal_Final_Image_angle"])

        self.ConfigureImage(postal)  # on enter create postal image

        self.canvas.after(settings["postal_Final_TimeUntilMoveToStart"] * 1000,
                          self.MoveToNextPage)  # move to next page

    def ResizeAnglePostal(self, postal, x, y, angle):
        postal = ImageTk.getimage(postal)  # convert to pil
        size = (x, y)
        postal = postal.resize(size, resample=Image.BICUBIC)  # resize it
        postal = postal.rotate(angle, expand=True, resample=Image.BICUBIC)
        postal = ImageTk.PhotoImage(postal)  # convert to photo image
        return postal

    def ConfigureImage(self, image):
        self.canvas.image = image  # <- Prevent garbage collection from deleting the image (tkinter is stupid)
        self.canvas.itemconfig(self.canvas_image, image=image)

    def MoveToNextPage(self):
        if self.active:
            self.controller.show_frame("StartPage")

    def ExitFrame(self):
        self.active = False
