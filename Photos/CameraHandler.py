import threading
from tkinter import *

import cv2
from PIL import Image, ImageTk


class CameraHandler:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.camera = cv2.VideoCapture(0)
                cls._instance.image = None
                cls._instance.is_recording = False
            return cls._instance

    @classmethod
    def Instance(cls):
        return cls()

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            threading.Thread(target=self._record_images, daemon=True).start()

    def stop_recording(self):
        self.is_recording = False

    def _record_images(self):
        while self.is_recording:
            ret, frame = self.camera.read()
            if not ret:
                print("Error reading from webcam.")
                break

            self.image = frame
            # cv2.imwrite("GeeksForGeeks.png", self.image)

    def ProcessImage(self):

        captured_image = Image.fromarray(self.image)
        photo_image = ImageTk.PhotoImage(image=captured_image)

        return photo_image

    def get_current_image(self):

        im = self.ProcessImage()

        return im
