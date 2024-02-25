import tkinter as tk  # python 3

var_readyTimer = 5
var_countdownTimer = 5

var_readyText = "Faz a tua composição"
var_countdownText = "Preparados ? "


class CompPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #########################################
        self.image_index = 0

        #self.readyTimer = var_readyTimer
        #self.countdownTimer = var_countdownTimer
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
        self.Image.bind("<Button-1>", lambda e: self.controller.show_frame("StartPage"))

        self.Instruction = tk.Label(
            self,
            text=var_readyText,
            font=controller.title_font)
        self.Instruction.place(
            x=900,
            y=800,
            anchor="center")

    def EnterFrame(self):
        self.active = True


        self.Instruction.config(text=var_readyText)
        self.ReadyTimer()
        self.ShowImage()

    def ShowImage(self):
        if self.active:
            webcam_image = self.controller.CreateFinalImage()

            self.ConfigureImage(webcam_image)
            self.Image.after(100, self.ShowImage)

    def CreateImage(self):
        image = self.controller.CreateFinalImage()
        self.ConfigureImage(image)

    def ReadyTimer(self):
        self.Instruction.after(var_readyTimer * 1000, self.Timer, var_countdownTimer)

    def Timer(self, countdown):

        if countdown >= 0:
            # call countdown again after 1000ms (1s)

            print("countdown = " + str(countdown))
            self.Instruction.config(text=var_countdownText + str(countdown))
            self.Instruction.after(1000, self.Timer, countdown - 1)

        if countdown < 0:
            self.controller.show_frame("ResultPage")

    def ConfigureImage(self, image):
        self.Image.configure(image=image)
        self.Image.image = image  # <- Prevent garbage collection from deleting the image (tkinter is stupid)

    def ExitFrame(self):
        self.active = False
