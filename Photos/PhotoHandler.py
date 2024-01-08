class PhotoHandler:

    def __init__(self):
        self.montageList = {}

    def addMontage(self, montage):
        self.montageList[montage.name] = montage
