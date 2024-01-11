import threading

import cv2


def CaptureCameraLoop(camPort=0):
    vid = cv2.VideoCapture(0)

    # Repeat each loop
    while (True):
        ret, frame = vid.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()


def CaptureCamera(camPort=0):
    vid = cv2.VideoCapture(camPort)
    result, image = vid.read()
    return image


'''
# Mono thead
while True:
    image2 = CaptureCamera()
    cv2.imshow('frame', image2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
'''

'''
# Running in a thead
t1 = threading.Thread(target=CaptureCameraLoop())
'''
