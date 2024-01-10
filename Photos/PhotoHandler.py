from Photos.Montage import Montage


class PhotoHandler:

    def __init__(self):
        self.montageList = {}

    def addMontage(self, montage):
        self.montageList[montage.name] = montage

    def createMontages(self):
        montage = Montage("teste", "25Abril", 1)

        self.montageList[montage.name] = montage


ph = PhotoHandler()
ph.createMontages()
ph.montageList["teste"].InsertUserImage("group1.jpg")
