import tkinter as tk  # python 3


class ChoosePage(tk.Frame):

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
            image=controller.images_choice[self.image_index]
            # image = None
        )
        self.Image.pack(
            fill="both",
            expand=True,
            # padx=(10, 10),
            # pady=(10,10),
            anchor="center",
        )

        ### BUTTONS ###
        # Middle Button
        self.selectButton = tk.Button(
            self,
            text="Gosto desta",
            command=lambda: self.controller.show_frame("CompPage"),
            font=controller.title_font)
        self.selectButton.place(
            x=900,
            y=800,
            anchor="center"
        )

        # Left Button
        buttonLeft = tk.Button(
            self,
            text="<<",
            command=lambda: self.NextImage(-1),
            font=controller.title_font)
        buttonLeft.place(
            x=800,
            y=800,
            anchor="center",
        )

        # Right Button
        buttonRight = tk.Button(
            self,
            text=">>",
            command=lambda: self.NextImage(1),
            font=controller.title_font
        )
        buttonRight.place(
            x=1000,
            y=800,
            anchor="center"
        )
        ### BUTTONS ###

    '''
    def NextImage(self):
        if self.image_index == len(self.controller.images_choice) - 1:
            self.Image.configure(image=self.controller.images_choice[0])
            self.image_index = 0
        else:
            self.Image.configure(image=self.controller.images_choice[self.image_index + 1])
            self.image_index += 1

    def PreviousImage(self):
        if self.image_index == 0:
            self.Image.configure(image=self.controller.images_choice[-1])
            self.image_index = len(self.controller.images_choice) - 1
        else:
            self.Image.configure(image=self.controller.images_choice[self.image_index - 1])
            self.image_index -= 1
    '''

    def NextImage(self, direction):
        image = self.controller.GetNextMontageCover(direction)
        self.ConfigureImage(image)

    def EnterFrame(self):
        self.active = True

        # Resetimg the image list to the first montage
        self.controller.SetMontageToFirst()

        image = self.controller.GetMontageCover()
        self.ConfigureImage(image)

    # Sets the image in the Image label
    def ConfigureImage(self, image):
        self.Image.configure(image=image)
        self.Image.image = image  # <- Prevent garbage collection from deleting the image (tkinter is stupid)

    def ExitFrame(self):
        self.active = False
