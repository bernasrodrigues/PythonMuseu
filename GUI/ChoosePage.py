import tkinter as tk  # python 3

from Settings.SettingsHandler import settings


class ChoosePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.active = False

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

        # Starting canvas image
        self.canvas_image = self.canvas.create_image(1080 / 2, 1980 / 2, anchor=tk.CENTER,
                                                     image=controller.images_choice[0])

        ### BUTTONS ###
        # Middle Button
        self.canvasChooseText = self.canvas.create_text(settings["choose_Title_X"],
                                                        settings["choose_Title_Y"],
                                                        text=settings["choose_Title_Text_PT"],
                                                        fill=settings['choose_Title_Fill'],
                                                        font=settings["choose_Title_Font"])
        self.canvas.tag_bind(self.canvasChooseText, '<Button-1>', lambda event: self.controller.show_frame("CompPage"))

        # Right Button
        self.rightArrowImage = tk.PhotoImage(file='arrow_right.png')

        self.canvas_rightButton = self.canvas.create_image(settings["choose_RightArrow_X"],
                                                           settings["choose_RightArrow_Y"],
                                                           anchor=tk.CENTER,
                                                           image=self.rightArrowImage)
        self.canvas.tag_bind(self.canvas_rightButton, '<Button-1>', lambda event: self.NextImage(1))

        # Left Button
        self.leftArrowImage = tk.PhotoImage(file='arrow_right.png')

        self.canvas_leftButton = self.canvas.create_image(settings["choose_LeftArrow_X"],
                                                          settings["choose_LeftArrow_Y"],
                                                          anchor=tk.CENTER,
                                                          image=self.leftArrowImage)
        self.canvas.tag_bind(self.canvas_leftButton, '<Button-1>', lambda event: self.NextImage(-1))

        # Language Select button
        # coordinates initially zero because they are set once all are created
        self.t1 = self.canvas.create_text(0, 0,
                                          text=settings["choose_SubTitle_PT"],
                                          anchor=tk.E,
                                          font=settings["choose_Subtitle_Font"])
        self.t2 = self.canvas.create_text(0, 0,
                                          text=settings["Choose_SubTitle_Separator"],
                                          anchor=tk.CENTER,
                                          font=settings["choose_Subtitle_Font"])
        self.t3 = self.canvas.create_text(0, 0,
                                          text=settings["choose_SubTitle_EN"],
                                          anchor=tk.W,
                                          font=settings["choose_Subtitle_Font"])

        # set the coordinates of the language select buttons
        self.canvas.coords(self.t1, settings["choose_Subtitle_X"] - 20, settings["choose_Subtitle_Y"])
        self.canvas.coords(self.t2, settings["choose_Subtitle_X"], settings["choose_Subtitle_Y"])
        self.canvas.coords(self.t3, settings["choose_Subtitle_X"] + 20, settings["choose_Subtitle_Y"])

        self.canvas.tag_bind(self.t1, '<Button-1>', lambda event: self.SetLang("_PT"))
        self.canvas.tag_bind(self.t3, '<Button-1>', lambda event: self.SetLang("_EN"))
        ### BUTTONS ###

    def NextImage(self, direction):
        image = self.controller.GetNextMontageCover(direction)
        self.ConfigureImage(image)

    def EnterFrame(self):
        self.active = True
        # Resetting the image list to the first montage
        self.controller.SetMontageToFirst()
        image = self.controller.GetMontageCover()
        self.ConfigureImage(image)

        self.UpdateLanguage()

    # Sets the image in the Image label
    def ConfigureImage(self, image):
        self.canvas.image = image  # <- Prevent garbage collection from deleting the image (tkinter is stupid)
        self.canvas.itemconfig(self.canvas_image, image=image)

    def SetLang(self, lang):
        self.controller.SetLang(lang)
        self.UpdateLanguage()

    def UpdateLanguage(self):

        lang = self.controller.language
        if lang == "_PT":
            self.canvas.itemconfigure(self.t1, font=settings["choose_Subtitle_Font_Bold"])
            self.canvas.itemconfigure(self.t3, font=settings["choose_Subtitle_Font"])

        if lang == "_EN":
            self.canvas.itemconfigure(self.t1, font=settings["choose_Subtitle_Font"])
            self.canvas.itemconfigure(self.t3, font=settings["choose_Subtitle_Font_Bold"])

        self.canvas.itemconfigure(self.canvasChooseText, text=settings["choose_Title_Text" + lang])

    def ExitFrame(self):
        self.active = False
