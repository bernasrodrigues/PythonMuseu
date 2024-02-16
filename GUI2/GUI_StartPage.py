import tkinter as tk  # python 3


class StartPage(tk.Frame):

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
            image=controller.images_intro[self.image_index]
        )
        self.Image.pack(
            fill="both",
            expand=True,
            # padx=(10, 10),
            # pady=(10,10),
            anchor="center"
        )
        # self.canvasImage.create_image(0, 0, image=controller.images_intro[self.image_index], anchor="nw")
        self.Image.bind("<Button-1>", lambda e: self.controller.show_frame("ChoosePage"))

        self.label = tk.Label(
            self,
            text="Toque no ecra para dar inicio à selfie",
            font=controller.title_font)
        self.label.place(
            x=900,
            y=800,
            anchor="center")

        """
        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        button2.pack()
        """

    def ImageCarrousel(self):

        if self.active:
            if self.image_index == len(self.controller.images_intro) - 1:
                self.Image.configure(image=self.controller.images_intro[self.image_index]) #anchor="nw")
                self.image_index = 0
            else:
                self.Image.configure(image=self.controller.images_intro[self.image_index]) #anchor="nw")
                self.image_index += 1

            self.Image.after(2000, self.ImageCarrousel)

    def EnterFrame(self):
        self.active = True
        self.ImageCarrousel()

    def ExitFrame(self):
        self.active = False
