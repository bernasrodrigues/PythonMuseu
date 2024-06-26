import tkinter as tk  # python 3

from PIL import Image, ImageTk

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
        self.canvas_image = self.canvas.create_image(1080 / 2, 1440 / 2, anchor=tk.CENTER,
                                                     image=None)

        # degrade
        self.canvas_degrade = self.canvas.create_image(1080 / 2, 1980 / 2,
                                                       anchor=tk.CENTER,
                                                       image=self.controller.degrade)

        ### BUTTONS ###
        # Middle Button
        self.canvasChooseText = self.canvas.create_text(settings["choose_Title_X"],
                                                        settings["choose_Title_Y"],
                                                        text=settings["choose_Title_Text_PT"],
                                                        fill=settings['choose_Title_Fill'],
                                                        font=settings["choose_Title_Font"])
        self.canvas.tag_bind(self.canvasChooseText, '<Button-1>', lambda event: self.controller.show_frame("CompPage"))

        # Right Button
        self.rightArrowImage = tk.PhotoImage(file='Images/Arrow_white_right.png')

        self.canvas_rightButton = self.canvas.create_image(settings["choose_RightArrow_X"],
                                                           settings["choose_RightArrow_Y"],
                                                           anchor=tk.CENTER,
                                                           image=self.rightArrowImage)
        self.canvas.tag_bind(self.canvas_rightButton, '<Button-1>', lambda event: self.NextImage(1))

        # Left Button
        self.leftArrowImage = tk.PhotoImage(file='Images/Arrow_white_left.png')

        self.canvas_leftButton = self.canvas.create_image(settings["choose_LeftArrow_X"],
                                                          settings["choose_LeftArrow_Y"],
                                                          anchor=tk.CENTER,
                                                          image=self.leftArrowImage)
        self.canvas.tag_bind(self.canvas_leftButton, '<Button-1>', lambda event: self.NextImage(-1))

        # Language Select button
        # coordinates initially zero because they are set once all are created
        self.canvas_t1 = self.canvas.create_text(0, 0,
                                                 text=settings["choose_SubTitle_PT"],
                                                 anchor=tk.E,
                                                 font=settings["choose_Subtitle_Font"])
        self.canvas_t2 = self.canvas.create_text(0, 0,
                                                 text=settings["Choose_SubTitle_Separator"],
                                                 anchor=tk.CENTER,
                                                 font=settings["choose_Subtitle_Font"],
                                                 fill=settings["choose_SubTitle_fill_deselected"])
        self.canvas_t3 = self.canvas.create_text(0, 0,
                                                 text=settings["choose_SubTitle_EN"],
                                                 anchor=tk.W,
                                                 font=settings["choose_Subtitle_Font"])

        # set the coordinates of the language select buttons
        self.canvas.coords(self.canvas_t1, settings["choose_Subtitle_X"] - 20, settings["choose_Subtitle_Y"])
        self.canvas.coords(self.canvas_t2, settings["choose_Subtitle_X"], settings["choose_Subtitle_Y"])
        self.canvas.coords(self.canvas_t3, settings["choose_Subtitle_X"] + 20, settings["choose_Subtitle_Y"])

        self.canvas.tag_bind(self.canvas_t1, '<Button-1>', lambda event: self.SetLang("_PT"))
        self.canvas.tag_bind(self.canvas_t3, '<Button-1>', lambda event: self.SetLang("_EN"))
        # -- BUTTONS --#

        self.fadeAfter = None

    '''
    pil objects for image effects
    tkinter widgets require photoImage objects
    '''

    def EnterFrame(self):
        self.active = True
        self.controller.SetMontageToFirst()  # Resetting the image list to the first montage

        self.fadeImage(0)

        # image = self.controller.GetMontageCover()
        # self.ConfigureImage(image)

        # self.ImageTransparency(1)
        self.UpdateLanguage()

    def fadeImage(self, alpha):

        if self.active:
            image = self.ImageTransparency(alpha)
            self.ConfigureImage(image)

            if alpha <= 1:  # repeat until fade in is done
                self.fadeAfter = self.canvas.after(10, self.fadeImage, alpha + 0.05)
            else:
                self.fadeAfter = self.canvas.after(10, self.fadeImageOut, alpha)

    def fadeImageOut(self, alpha):
        if self.active:
            image = self.ImageTransparency(alpha)
            self.ConfigureImage(image)

            if alpha >= 0:  # repeat until all fade is done
                self.fadeAfter = self.canvas.after(10, self.fadeImageOut, alpha - 0.05)
            else:
                self.fadeAfter = self.canvas.after(10, self.fadeImage, alpha)

    def ImageTransparency(self, alpha):
        imageOriginal = self.controller.GetMontageCover()  # ImageTk.PhotoImage format
        imageUserIndicator = self.controller.GetMontageExample()

        imageOriginal = ImageTk.getimage(imageOriginal)  # convert to pil
        imageUserIndicator = ImageTk.getimage(imageUserIndicator)  # convert to pil

        # ex = ImageTk.getimage(ex)                                             # convert photoimage to pil
        # ex = ImageTk.PhotoImage(ex)                                           # convert pil to photoimage

        image = Image.blend(imageOriginal, imageUserIndicator, alpha)
        # image.save("AAAAA.png")

        image = ImageTk.PhotoImage(image)
        return image

    def NextImage(self, direction):
        self.canvas.after_cancel(self.fadeAfter)
        self.controller.GetNextMontageCover(direction)
        self.fadeImage(0)  # fade in configures the image
        # self.ConfigureImage(image)

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
            self.canvas.itemconfigure(self.canvas_t1, font=settings["choose_Subtitle_Font_Bold"],
                                      fill=settings["choose_SubTitle_fill_selected"])
            self.canvas.itemconfigure(self.canvas_t3, font=settings["choose_Subtitle_Font"],
                                      fill=settings["choose_SubTitle_fill_deselected"])

        if lang == "_EN":
            self.canvas.itemconfigure(self.canvas_t1, font=settings["choose_Subtitle_Font"],
                                      fill=settings["choose_SubTitle_fill_deselected"])
            self.canvas.itemconfigure(self.canvas_t3, font=settings["choose_Subtitle_Font_Bold"],
                                      fill=settings["choose_SubTitle_fill_selected"])

        self.canvas.itemconfigure(self.canvasChooseText, text=settings["choose_Title_Text" + lang])

    def ExitFrame(self):
        self.canvas.after_cancel(self.fadeAfter)
        self.active = False
