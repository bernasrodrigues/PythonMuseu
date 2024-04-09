import tkinter as tk  # python 3
import keyboard

from Settings.SettingsHandler import settings


class PostalPageFinal(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #########################################
        self.image_index = 0
        self.active = False
        self.barCode = ""

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

        self.canvas_text = self.canvas.create_text(500,
                                                   500,
                                                   text="Obrigado",
                                                   fill="white",
                                                   font=settings["comp_Title_Font"])

        self.canvas_text = self.canvas.create_text(500,
                                                   600,
                                                   text="A tua selfie já está disponivel",
                                                   fill="white",
                                                   font=settings["comp_Title_Font"])

        self.canvas.bind("<Button-1>", lambda e: self.controller.show_frame("StartPage"))
        # self.canvas.bind("<Key>", self.KeyPress)
        keyboard.on_press(self.on_barcode_scan)

    def EnterFrame(self):
        self.active = True
        self.ConfigureImage(self.controller.GetPostalMontageImage())
        print("Showing Postal Final Image")
        # self.canvas.after(10000, self.MoveToNextPage)

    def ConfigureImage(self, image):
        self.canvas.image = image  # <- Prevent garbage collection from deleting the image (tkinter is stupid)
        self.canvas.itemconfig(self.canvas_image, image=image)

    # Listen for barcode scanner input events
    def on_barcode_scan(self, event):
        if self.active:
            if event.name == 'enter':
                print("Enter key pressed")
                print("Final barcode:", self.barCode)
                self.controller.SavePostalImage(self.barCode)

            else:
                self.barCode += event.name
                # Handle barcode scanning
                print("Barcode scanned:", self.barCode)

    '''
    def KeyPress(self, event):

        if event.char in '0123456789':
            self.controller.barCode += event.char
            # print('>', code)
            print(self.controller.barCode)

        elif event.keysym == 'Return':
            # print('result:', code)
            print("barcode end: " + self.controller.barCode)
            self.controller.barCode = ""
    '''

    # automatically move to next page if not clicked
    def MoveToNextPage(self):
        pass

    def ExitFrame(self):
        self.active = False
