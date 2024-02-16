import tkinter as tk  # python 3


class ResultPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #########################################
        self.image_index = 0
        self.active = False

        self.Image = tk.Label(
            self,
            # width=1000,
            # height=1000
            image=controller.images_intro[0]
        )
        self.Image.pack(
            fill="both",
            expand=True,
            # padx=(10, 10),
            # pady=(10,10),
            anchor="center"
        )
        # self.canvasImage.create_image(0, 0, image=controller.images_intro[self.image_index], anchor="nw")
        self.Image.bind("<Button-1>", lambda e: self.controller.show_frame("StartPage"))

        self.label = tk.Label(
            self,
            text="Resultado",
            font=controller.title_font)
        self.label.place(
            x=900,
            y=800,
            anchor="center")

        self.pageLabel = tk.Label(
            self,
            text="Results Page",
            font=controller.title_font)
        self.pageLabel.place(
            x=0,
            y=0,
            anchor="nw")

    def EnterFrame(self):
        self.active = True
        self.ConfigureImage(self.controller.GetFinalImage())

    def ConfigureImage(self, image):
        self.Image.configure(image=image)
        self.Image.image = image  # <- Prevent garbage collection from deleting the image (tkinter is stupid)

    def ExitFrame(self):
        self.active = False
