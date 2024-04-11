import tkinter as tk  # python 3

from Settings.SettingsHandler import settings


# NOT USED

class CompPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.active = False
        self.inCountdown = False

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
        # creating empty image holder to be filled with the montage images
        self.canvas_image = self.canvas.create_image(1080 / 2, 1440 / 2, anchor=tk.CENTER)

        # degrade
        self.canvas_degrade = self.canvas.create_image(1080 / 2, 1980 / 2,
                                                       anchor=tk.CENTER,
                                                       image=self.controller.degrade)

        # text for the user
        self.canvas_text = self.canvas.create_text(settings["comp_Title_X"],
                                                   settings["comp_Title_Y"],
                                                   text=settings["comp_Ready_Text_PT"],
                                                   fill=settings['comp_Title_Fill'],
                                                   font=settings["comp_Title_Font"])

        self.canvas_text_countdown = self.canvas.create_text(settings["comp_Timer_X"],
                                                             settings["comp_Timer_Y"],
                                                             text="",
                                                             fill=settings["comp_Title_Fill"],
                                                             font=settings["comp_Timer_Font"])

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

    def EnterFrame(self):
        self.active = True
        self.StartTimer()  # Set user warn timer
        self.ShowImage("segmentation")  # shows photo combined with the webcam user image
        self.inCountdown = False
        self.canvas.itemconfig(self.canvas_text_countdown, text="")  # reset countdown text
        self.UpdateLanguage()

    # Updates the generated image every x seconds
    def ShowImage(self, function):
        if self.active:
            userMontageImage = self.controller.CreateUserMontageImage(function)
            self.ConfigureImage(userMontageImage)
            self.canvas.after(100, self.ShowImage, function)

    # After the user ready timer starts the countdown timer and configures the text
    def StartTimer(self):
        self.canvas.itemconfig(self.canvas_text, text=settings["comp_Ready_Text" + self.controller.language])
        self.canvas.after(settings["comp_readyTimer"] * 1000, self.Timer,
                          settings["comp_countdownTimer"])  # start the ready timer after the time set in the settings

    # Starts user ready timer after the set time has passed it starts the countdown timer
    def Timer(self, countdown):
        self.canvas.itemconfig(self.canvas_text, text=settings["comp_CountDown_Text" + self.controller.language])
        self.inCountdown = True
        if countdown >= 1:
            print("countdown = " + str(countdown))
            self.canvas.itemconfig(self.canvas_text_countdown, text=countdown)
            self.canvas.after(1000, self.Timer, countdown - 1)  # call countdown again after 1000ms (1s)

        else:
            self.ShowImage("rembg")
            self.controller.show_frame("PostalPage")

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

        if self.inCountdown:
            self.canvas.itemconfigure(self.canvas_text, text=settings["comp_CountDown_Text" + self.controller.language])
        else:
            self.canvas.itemconfigure(self.canvas_text, text=settings["comp_Ready_Text" + self.controller.language])

    def ExitFrame(self):
        self.active = False
        self.inCountdown = False
