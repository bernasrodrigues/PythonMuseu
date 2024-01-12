import threading

import cv2
import numpy
from PIL.ImageFile import ImageFile

from Photos import CameraCapture
from Photos.Montage import Montage


class PhotoHandler:

    def __init__(self):
        self.montageList = {}

    def addMontage(self, montage):
        self.montageList[montage.name] = montage

    def createMontages(self):
        montage = Montage("teste", "25Abril", 1)

        self.montageList[montage.name] = montage


'''
ph = PhotoHandler()
ph.createMontages()
ph.montageList["teste"].InsertUserImage("group1.jpg")
'''
#ImageFile.LOAD_TRUNCATED_IMAGES = True

ph = PhotoHandler()
ph.createMontages()

t1 = threading.Thread(target=CameraCapture.CameraCaptureAAA)
t1.start()

while True:
    if CameraCapture.camImage is not None:
        im = ph.montageList["teste"].InsertUserImage2(CameraCapture.camImage)
        im2 = ph.montageList["teste"].CreateFinalImage2(im)

        cv2Img = numpy.array(im2)
        # a = cv2.imread("teste_finalImage.png")
        cv2.imshow("frame", cv2Img)

        if cv2.waitKey(2) & 0xFF == ord('q'):
            t1.join()
            break

# CameraCapture.CameraCapture(0)
'''
while True:
    # ph.montageList["teste"].InsertUserImage("group1.jpg")
    if CameraCapture.camImage is not None:

        # print(CameraCapture.camImage)
        ph.montageList["teste"].InsertUserImage2(CameraCapture.camImage)

        # cv2.imshow('frame', ph.montageList["teste"].finalImage)
        im = cv2.imread(ph.montageList["teste"].name + "_finalImage.png")
        cv2.imshow('frame', im)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
'''
