import tkinter as tk

from Settings.SettingsHandler import settings


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.image_index = 0
        self.active = False
        self.imageCarrousel = None

        ### Canvas ###
        # Canvas
        self.canvas = tk.Canvas(
            self,
            width=1080,
            height=1980,
            background='gray'

        )
        self.canvas.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER
        )

        # Background image creation
        self.canvas_image = self.canvas.create_image(1080 / 2, 1980 / 2, anchor=tk.CENTER,
                                                     image=self.controller.images_intro[0])
        ### Text ###
        # Main title text
        self.canvas_title = self.canvas.create_text(settings["start_Title_X"],
                                                    settings["start_Title_Y"],
                                                    text=settings["start_Title_Text"],
                                                    fill=settings['start_Title_Fill'],
                                                    font=settings["start_Title_Font"])

        # Portuguese subtitles
        self.canvas_subtitle_PT = self.canvas.create_text(settings["start_Subtitle_PT_X"],
                                                          settings["start_Subtitle_PT_Y"],
                                                          text=settings["start_Subtitle_PT_Text"],
                                                          fill=settings['start_Subtitle_PT_Fill'],
                                                          font=settings["start_Subtitle_PT_Font"],
                                                          anchor="nw")

        # English subtitles

        self.canvas_subtitle_EN = self.canvas.create_text(settings["start_Subtitle_EN_X"],
                                                          settings["start_Subtitle_EN_Y"],
                                                          text=settings["start_Subtitle_EN_Text"],
                                                          fill=settings['start_Subtitle_EN_Fill'],
                                                          font=settings["start_Subtitle_EN_Font"],
                                                          anchor="nw")

        self.canvas.bind("<Button-1>", lambda e: self.controller.show_frame("ChoosePage"))

    def EnterFrame(self):
        self.active = True

        if self.imageCarrousel is not None:
            self.after_cancel(self.imageCarrousel)
        self.ImageCarrousel()

    def ImageCarrousel(self):
        if self.active:
            if self.image_index == len(self.controller.images_intro) - 1:
                self.canvas.itemconfig(self.canvas_image, image=self.controller.images_intro[self.image_index])
                self.image_index = 0

            else:
                self.canvas.itemconfig(self.canvas_image, image=self.controller.images_intro[self.image_index])
                self.image_index += 1

            self.imageCarrousel = self.canvas.after(settings["start_ImageCarrousel_Timer"], self.ImageCarrousel)

    def ExitFrame(self):
        if self.imageCarrousel is not None:
            self.after_cancel(self.imageCarrousel)
        self.active = False
