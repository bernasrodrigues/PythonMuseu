import threading
import time
from tkinter import *

import cv2
from PIL import Image, ImageTk
from pynput import mouse

from Settings.SettingsHandler import settings


class MouseListener:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)

                # cls._instance.controller = controller
                cls._instance.controller = None

                cls._instance.listener = None
                print("Created Mouse Listener\n------------")
            return cls._instance

    @classmethod
    def Instance(cls):
        return cls()

    def AssignController(self, controller):
        self.controller = controller

    def On_click(self, x, y, button, pressed):
        # x , y -> mouse position
        # button -> ???
        # pressed if the button is pressed (true/false)

        if pressed:
            self.controller.refreshTimer(settings["pageTimeout"])

    def Start(self):
        self.listener = mouse.Listener(on_click=self.On_click)
        self.listener.start()

    def Stop(self):
        self.listener.stop()
        self.listener.join()
