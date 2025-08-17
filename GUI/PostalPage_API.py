import threading
import tkinter as tk  # python 3

import keyboard
from PIL import ImageTk, Image

from APIGetter.APIClientWorker import APIClientWorker
from QRGenerator.QRgenerator import QRGenerator
from Settings.SettingsHandler import settings


class PostalPage_API(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #########################################
        self.image_index = 0
        self.active = False
        self.barCode = ""

        self.currentText = "postal_API_Title_Text"

        ### Canvas ###
        # Canvas
        self.canvas = tk.Canvas(
            self,
            width=1080,
            height=1980,
            background='black'

        )
        self.canvas.place(
            relx=0.5,
            rely=0.5,
            anchor=tk.CENTER
        )

        # Final image presentation initially set to none
        self.canvas_image = self.canvas.create_image(settings["postal_Image_X"],
                                                     settings["postal_Image_Y"],
                                                     anchor=tk.CENTER,
                                                     image=None)

        self.canvas_text = self.canvas.create_text(settings["postal_API_Title_X"],
                                                   settings["postal_API_Title_Y"],
                                                   text=settings[self.currentText + self.controller.language],
                                                   fill=settings["postal_API_Title_Fill"],
                                                   font=settings["postal_API_Title_Font"])

        self.canvas_qr = self.canvas.create_image(settings["postal_API_QR_X"],  # define this in settings, e.g., 200
                                                  settings["postal_API_QR_Y"],  # define this in settings, same Y as text
                                                  anchor=tk.CENTER,
                                                  image=None)

        '''
        # degrade
        self.canvas_degrade = self.canvas.create_image(1080 / 2, 1980 / 2,
                                                       anchor=tk.CENTER,
                                                       image=self.controller.degrade)
        '''

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

        # self.canvas.bind("<Button-1>", lambda e: self.controller.show_frame("PostalPageFinal"))

    # Call API worker to fech data from the API
    def fetch_data(self):
        APIClientWorker.Instance().request_api_call()
        data = APIClientWorker.Instance().get_response_data()

        print("API Response Data:", data)

        if data:
            self.currentText = "postal_API_Scan_QR_Text"
            # Generate QR code from data
            qr_img = QRGenerator.Instance().generate_qr(data)

            # Convert PIL Image to Tkinter PhotoImage
            qr_img = qr_img.resize((250, 250))  # resize QR code if needed
            qr_photo = ImageTk.PhotoImage(qr_img)

            # Update UI from main thread
            def update_ui():
                self.canvas.itemconfigure(
                    self.canvas_text,
                    text=settings[self.currentText + self.controller.language]
                )
                self.canvas_qr_image = qr_photo  # Prevent GC
                self.canvas.itemconfigure(self.canvas_qr, image=self.canvas_qr_image)

            self.canvas.after(0, update_ui)

        else:
            self.currentText = "postal_API_ERROR_Text"
            # Handle error case
            self.canvas.after(0, lambda: self.canvas.itemconfigure(
                self.canvas_text,
                text=settings[self.currentText + self.controller.language]
            ))

        APIClientWorker.Instance().close_session()

    def EnterFrame(self):
        self.active = True
        self.barCode = ""  # reset barcode
        print("Showing Postal Image API")

        # create postal , resize and set the image to postal
        postal = self.controller.CreatePostalMontageImage()
        postal = self.ResizePostal(postal, settings["postal_API_Image_resize_X"], settings["postal_API_Image_resize_Y"])
        # postal = self.ResizePostal(postal, 500, 500)

        self.ConfigureImage(postal)  # on enter create postal image

        # keyboard.on_press(self.on_barcode_scan)  # start listening to keyboard
        # self.canvas.after(20000, self.MoveToNextPage)           # move to next page
        self.UpdateLanguage()

        threading.Thread(target=self.fetch_data, daemon=True).start()  # call API

    def ResizePostal(self, postal, x, y):
        postal = ImageTk.getimage(postal)  # convert to pil
        size = (x, y)
        postal = postal.resize(size, resample=Image.BICUBIC)  # resize it
        postal = ImageTk.PhotoImage(postal)  # convert to photo image
        return postal

    def ConfigureImage(self, image):
        self.canvas.image = image  # <- Prevent garbage collection from deleting the image (tkinter is stupid)
        self.canvas.itemconfig(self.canvas_image, image=image)

    '''
    def on_barcode_scan(self, event):
        if self.active:
            if event.name == 'enter':
                print("Enter key pressed")
                print("Final barcode:", self.barCode)
                self.controller.SavePostalImage(self.barCode)

                self.barCode = ""  # reset barcode (just to be safe)

                self.controller.show_frame("PostalPageFinal")

            else:
                self.barCode += event.name
                # Handle barcode scanning
                print("Barcode scanned:", self.barCode)
    '''

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

        self.canvas.itemconfigure(self.canvas_text, text=settings[self.currentText + self.controller.language])

    # automatically move to next page if not clicked
    def MoveToNextPage(self):
        if self.active:
            self.controller.show_frame("Start")

    def ExitFrame(self):
        # keyboard.unhook_all()  # stop listening to keyboard
        self.active = False
