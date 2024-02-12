import threading
from time import sleep
import cv2



### OLD DO NOT USE
'''
def Initialize():
    PhotoHandler.cameraThread.start()


def pause():
    PhotoHandler.running = True
    # If in sleep, we acquire immediately, otherwise we wait for thread
    # to release condition. In race, worker will still see self.paused
    # and begin waiting until it's set back to False
    PhotoHandler.pause_cond.acquire()


# should just resume the thread
def resume(self):
    PhotoHandler.running = True
    # Notify so thread will wake after lock released
    PhotoHandler.pause_cond.notify()
    # Now release the lock
    PhotoHandler.pause_cond.release()


def CameraCapture():
    vid = cv2.VideoCapture(0)
    while True:
        with PhotoHandler.pause_cond:
            while PhotoHandler.running:
                PhotoHandler.pause_cond.wait()
                ret, frame = vid.read()
                PhotoHandler.cameraImage = frame
        sleep(0.5)
'''


class PhotoHandler:
    @classmethod
    def Initialize(cls):
        PhotoHandler.cameraThread.start()

    @classmethod
    def pause(cls):
        PhotoHandler.running = False
        # If in sleep, we acquire immediately, otherwise we wait for thread
        # to release condition. In race, worker will still see self.paused
        # and begin waiting until it's set back to False
        PhotoHandler.pause_cond.acquire()

    # should just resume the thread
    @classmethod
    def resume(cls):
        PhotoHandler.running = True
        # Notify so thread will wake after lock released
        PhotoHandler.pause_cond.notify()
        # Now release the lock
        PhotoHandler.pause_cond.release()

    @classmethod
    def CameraCapture(cls):
        vid = cv2.VideoCapture(0)
        while True:
            with PhotoHandler.pause_cond:
                while PhotoHandler.running:
                    PhotoHandler.pause_cond.wait()
                    ret, frame = vid.read()
                    PhotoHandler.cameraImage = frame
            sleep(0.5)

    cameraImage = None
    pause_cond = threading.Condition(threading.Lock())
    running = False
    cameraThread = threading.Thread(target=CameraCapture)


'''
class PhotoHandler:

    def __init__(self):
        self.montageList = {}

    def addMontage(self, montage):
        self.montageList[montage.name] = montage

    def createMontages(self):
        montage = Montage("teste", "25Abril", 1)

        self.montageList[montage.name] = montage

    def cameraCapture(self):
        pass


'''

'''
ph = PhotoHandler()
ph.createMontages()
ph.montageList["teste"].InsertUserImage("group1.jpg")
'''

'''
# ImageFile.LOAD_TRUNCATED_IMAGES = True

ph = PhotoHandler()
ph.createMontages()

t1 = threading.Thread(target=CameraCapture.CameraCaptureAAA)
t1.start()

while True:
    if CameraCapture.camImage is not None:
        im = ph.montageList["teste"].InsertUserImage2(CameraCapture.camImage)
        im = im.convert("LA")  # convert to grayscale
        im2 = ph.montageList["teste"].CreateFinalImage2(im)

        cv2Img = numpy.array(im2)
        # a = cv2.imread("teste_finalImage.png")
        cv2.imshow("frame", cv2Img)

        if cv2.waitKey(2) & 0xFF == ord('q'):
            t1.join()
            break

# CameraCapture.CameraCapture(0)
'''

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
'''
'''
