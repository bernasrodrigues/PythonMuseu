import threading

import cv2

camImage = None


def CameraCaptureContinuous(camPort=0):
    vid = cv2.VideoCapture(0)

    # Repeat each loop
    while True:
        ret, frame = vid.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


def CameraCaptureSingle(camPort=0):
    vid = cv2.VideoCapture(camPort)
    result, image = vid.read()
    return image


def CameraCaptureAAA(camPort=0):
    vid = cv2.VideoCapture(0)

    # Repeat each loop
    while True:
        ret, frame = vid.read()
        global camImage
        camImage = frame
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


'''
# Mono thead
while True:
    image2 = CameraCaptureSingle()
    cv2.imshow('frame', image2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''

'''
# Running in a thead
t1 = threading.Thread(target=CameraCaptureContinuous())
'''
