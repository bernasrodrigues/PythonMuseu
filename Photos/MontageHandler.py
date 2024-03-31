import os
import threading

from Photos.Montage import Montage
from Photos.MontageFunctions import MontagebasePlacement, MontageBaseEffect


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

                cls._instance.montageList["Montagem1"] = Montage("Montagem1", MontagebasePlacement, MontageBaseEffect)
                cls._instance.montageList["Montagem2"] = Montage("Montagem2", MontagebasePlacement, MontageBaseEffect)
                cls._instance.montageList["Montagem3"] = Montage("Montagem3", MontagebasePlacement, MontageBaseEffect)
                cls._instance.montageList["Montagem4"] = Montage("Montagem4", MontagebasePlacement, MontageBaseEffect)
                cls._instance.montageList["Montagem5"] = Montage("Montagem5", MontagebasePlacement, MontageBaseEffect)

            return cls._instance

    @classmethod
    def Instance(cls):
        return cls()

    # Not used
    def GetMontageCoverImage(self, MontageName):
        montage = self.montageList[MontageName]
        return montage.GetCoverImage()

    def GetMontage(self, MontageName):
        return self.montageList[MontageName]

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

    def CreateMontageUserImage(self, image):
        self.montageList[self.currentMontage].createUserMontageImage(image)
        return self.montageList[self.currentMontage].userMontageImage

    def CreateMontagePostalImage(self):
        self.montageList[self.currentMontage].CreatePostalImage()
        return self.montageList[self.currentMontage].finalImage

    def SetMontageToFirst(self):
        if not self.montageList:
            return None
        # Set currentMontage to the first element in MontageList
        self.currentMontage = next(iter(self.montageList))
        # print(self.currentMontage)

    def GetCurrentMontageCoverImage(self):
        return self.montageList[self.currentMontage].coverImage

    def GetCurrentMontage(self):
        return self.montageList[self.currentMontage]

    # def Get_NextItem(self):

    def GetUserMontageImage(self):
        return self.montageList[self.currentMontage].userMontageImage
