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

    def StartRecording(self):
        if not self.is_recording:
            self.is_recording = True
            threading.Thread(target=self._RecordImages, daemon=True).start()

    def StopRecording(self):
        self.is_recording = False

    def _RecordImages(self):
        while self.is_recording:
            ret, frame = self.camera.read()
            if not ret:
                print("Error reading from webcam.")
                break

            opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            self.image = opencv_image
            # cv2.imwrite("GeeksForGeeks.png", self.image)

    # The recorded webcam image appears mirrored, applies a flip effect to the image to appear as expected
    def FlipImage(self):

        flip_img = cv2.flip(self.image, 1)
        captured_image = Image.fromarray(flip_img)
        photo_image = ImageTk.PhotoImage(image=captured_image)

        return photo_image

    # Returns the raw image from the camera (image from the camera is mirrored)
    def GetRawImage(self):
        return self.image

    # Applies effects to the camera to appear more natural
    def GetProcessedImage(self):

        im = self.FlipImage()
        # TODO ADD MORE EFFECTS TO THE IMAGE

        return im

    def GetPilImage(self):

        flip_img = cv2.flip(self.image, 1)
        pil_image = Image.fromarray(flip_img)
        return pil_image

