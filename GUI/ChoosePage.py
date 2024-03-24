import tkinter as tk  # python 3


class ChoosePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #########################################
        self.image_index = 0
        self.active = False

        self.canvas = tk.Canvas(
            self,
            width=1080,
            height=1980,
            background='red'
        )

        self.canvas.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER
        )

        self.canvas_image = self.canvas.create_image(1080 / 2, 1980 / 2, anchor=tk.CENTER,
                                                     image=controller.images_choice[self.image_index])

        '''
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
        '''


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
            anchor=tk.CENTER
        )

        # Left Button
        buttonLeft = tk.Button(
            self,
            text="<",
            command=lambda: self.NextImage(-1),
            font=controller.title_font)
        buttonLeft.place(
            x=800,
            y=800,
            anchor=tk.CENTER,
        )

        # Right Button
        buttonRight = tk.Button(
            self,
            text=">",
            command=lambda: self.NextImage(1),
            font=controller.title_font
        )
        buttonRight.place(
            x=1000,
            y=800,
            anchor=tk.CENTER
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
        return

        image = self.controller.GetNextMontageCover(direction)
        self.ConfigureImage(image)

    def EnterFrame(self):
        self.active = True
        return
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
