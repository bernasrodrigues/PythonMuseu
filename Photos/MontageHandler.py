import os
import threading

from Photos.Montage import Montage
from Photos.MontageFunctions import MontageBasePlacement, MontageBaseEffect, MontageBaseResize, MontageColorizeEffect, \
    ColorizeEffect, MontagePerspectiveTransformResize


class MontageHandler:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super().__new__(cls)
                cls._instance.montageList = {}
                cls._instance.currentMontage = None

                # Get list of directories names in the current directory
                # TODO AUTOMATE THIS
                '''
                current_directory = os.getcwd()
                # Get all directory names in the current directory
                folders = [d for d in os.listdir(current_directory) if
                               os.path.isdir(os.path.join(current_directory, d))]
                for folder_name in folders:
                    cls._instance.MontageList[folder_name] = Montage(folder_name)
                '''
                m1 = Montage("Montagem1",
                             MontageBasePlacement,
                             MontageBaseResize,
                             MontageBaseEffect)
                cls._instance.montageList["Montagem1"] = m1

                m2 = Montage("Montagem2",
                             MontageBasePlacement,
                             MontagePerspectiveTransformResize,
                             MontageBaseEffect)

                m2.postalAdditionalEffects = ColorizeEffect

                cls._instance.montageList["Montagem2"] = m2

                m3 = Montage("Montagem3",
                             MontageBasePlacement,
                             MontageBaseResize,
                             MontageBaseEffect)
                cls._instance.montageList["Montagem3"] = m3

                m4 = Montage("Montagem4",
                             MontageBasePlacement,
                             MontageBaseResize,
                             MontageBaseEffect)
                cls._instance.montageList["Montagem4"] = m4

                m5 = Montage("Montagem5",
                             MontageBasePlacement,
                             MontageBaseResize,
                             MontageBaseEffect)

                cls._instance.montageList["Montagem5"] = m5

            return cls._instance

    @classmethod
    def Instance(cls):
        return cls()

    def GetMontage(self, MontageName):
        return self.montageList[MontageName]

    def GetMontageCoverImage(self, MontageName):
        montage = self.montageList[MontageName]
        return montage.GetCoverImage()

    def GetMontageExampleImage(self, MontageName):
        montage = self.montageList[MontageName]
        return montage.GetExampleImage()

    def GetNextElement(self, direction):
        # Check if MontageList is empty
        if not self.montageList:
            return None

        # If currentMontage is None or not in MontageList, set it to the first element
        if self.currentMontage is None or self.currentMontage not in self.montageList:
            self.SetMontageToFirst()

        # Get the keys of MontageList
        montage_keys = list(self.montageList.keys())

        # Calculate the index of the next Montage, wrapping around to the beginning if necessary
        next_index = (montage_keys.index(self.currentMontage) + direction) % len(montage_keys)

        # Update currentMontage with the next Montage key
        self.currentMontage = montage_keys[next_index]

        # Return the corresponding Montage object
        return self.montageList[self.currentMontage]

    def SetMontageToFirst(self):
        if not self.montageList:
            return None
        # Set currentMontage to the first element in MontageList
        self.currentMontage = next(iter(self.montageList))
        # print(self.currentMontage)

    def GetCurrentMontageCoverImage(self):
        return self.montageList[self.currentMontage].GetCoverImage()

    def GetCurrentMontageExampleImage(self):
        return self.montageList[self.currentMontage].GetExampleImage()

    def GetCurrentMontage(self):
        return self.montageList[self.currentMontage]

    def CreateMontageUserImage(self, image, function):  # Inserts the user image in the montage
        self.montageList[self.currentMontage].createUserMontageImage(image, function)
        return self.montageList[self.currentMontage].userMontageImage

    def GetUserMontageImage(self):  # Gets the current montage user image
        return self.montageList[self.currentMontage].userMontageImage

    def CreateMontagePostalImage(self):  # Create the user postal image
        self.montageList[self.currentMontage].CreatePostalImage()
        return self.montageList[self.currentMontage].finalImage

    def GetPostalMontageImage(self):  # Gets the user postal image
        return self.montageList[self.currentMontage].finalImage
