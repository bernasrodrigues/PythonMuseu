import tkinter as tk  # python 3


class PostalPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #########################################
        self.image_index = 0
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

        # Final image presentation initially set to none
        self.canvas_image = self.canvas.create_image(1080 / 2, 1980 / 2, anchor=tk.CENTER, image=None)

        '''
        # degrade
        self.canvas_degrade = self.canvas.create_image(1080 / 2, 1980 / 2,
                                                       anchor=tk.CENTER,
                                                       image=self.controller.degrade)
        '''

        self.canvas.bind("<Button-1>", lambda e: self.controller.show_frame("StartPage"))

    def EnterFrame(self):
        self.active = True
        self.ConfigureImage(self.controller.CreatePostalMontageImage())
        print("Showing Postal Image")

        #self.canvas.after(10000, self.MoveToNextPage)

    def ConfigureImage(self, image):
        self.canvas.image = image  # <- Prevent garbage collection from deleting the image (tkinter is stupid)
        self.canvas.itemconfig(self.canvas_image, image=image)

    # automatically move to next page if not clicked
    def MoveToNextPage(self):
        pass

    def ExitFrame(self):
        self.active = False
