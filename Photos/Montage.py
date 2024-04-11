import os

import cv2
import cvzone
import numpy
import numpy as np
import rembg
from PIL import Image, ImageOps
from cvzone.SelfiSegmentationModule import SelfiSegmentation

from Photos.MontageFunctions import resize
from Settings.SettingsHandler import settings

# A Montage contains the list of layers that compose an Image
# the user images is inserted in the position that we want it to be
segmentor = SelfiSegmentation()


class Montage:

    def __init__(self, folder, placementFunct, resizeFunct, effectFunct):
        self.name = folder  # Name for the montage
        self.coverImage = None  # Original image
        self.frontImage = None  # Image in front of the user
        self.exampleImage = None  # Image of the user
        self.userMontageImage = None  # Final generated image
        self.postalImage = None  # image of the postal
        self.finalImage = None  # final image on the postal

        # functions to apply Effects
        self.placementFunct = placementFunct
        self.effectFunct = effectFunct
        self.resizeFunct = resizeFunct

        print(f"Creating Montage for {folder}")

        currentDirectory = os.path.dirname(os.path.abspath(__file__))
        currentDirectory = os.path.join(currentDirectory, folder)
        allFilesInDir = [os.path.join(currentDirectory, file_name) for file_name in os.listdir(currentDirectory) if
                         os.path.isfile(os.path.join(currentDirectory, file_name))]

        for fileName in allFilesInDir:
            imageName = os.path.basename(fileName)  # Check layer name

            match os.path.basename(fileName):
                case "cover.png":
                    self.coverImage = Image.open(fileName).convert('RGBA')
                    print(f"Image {imageName} added as cover")
                case "topo.png":
                    self.frontImage = Image.open(fileName).convert('RGBA')
                    print(f"Image {imageName} added as cover")
                case "user.png":
                    self.exampleImage = Image.open(fileName).convert('RGBA')
                    print(f"Image {imageName} added as cover")
                case "postal.png":
                    self.postalImage = Image.open(fileName).convert('RGBA')
                    print(f"Image {imageName} added as postal")

            '''
            if os.path.basename(fileName) == "cover.png":  # add cover image
                self.coverImage = Image.open(fileName).convert('RGBA')
                print(f"Image {imageName} added as cover")

            elif os.path.basename(fileName) == "topo.png":  # add front image
                self.frontImage = Image.open(fileName).convert('RGBA')
                print(f"Image {imageName} added as front image")

            elif os.path.basename(fileName) == "user.png":  # add example image
                self.exampleImage = Image.open(fileName).convert('RGBA')
                print(f"Image {imageName} added as example image")  # leave space for the user image
            '''

        print(f"Montage {folder} created\n---------------------")

    def GetCoverImage(self):
        return self.coverImage

    def GetExampleImage(self):
        return self.exampleImage

    def RemBGRemove(self, userImage):  # Removing using rembg
        userImageWithoutBackground = rembg.remove(userImage)

        return userImageWithoutBackground

    def SelfieSegmentationRemove(self, userImage):

        userImage = numpy.array(userImage)
        userImage = userImage[:, :, :3]  # remove alpha channel

        color = (255, 0, 255)
        imgOut = segmentor.removeBG(userImage, imgBg=color, cutThreshold=0.1)

        mask = np.where((imgOut == color).all(axis=2), 0, 255).astype(np.uint8)

        result = imgOut.copy()
        result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
        result[:, :, 3] = mask

        userImage = Image.fromarray(result)
        return userImage

    # User image -> file path to the user image
    def createUserMontageImage(self, userImage, function):
        # TODO

        if function == "rembg":
            userImageWithoutBackground = self.RemBGRemove(userImage)
        if function == "segmentation":
            userImageWithoutBackground = self.SelfieSegmentationRemove(userImage)

        self.InsertUserImage(userImageWithoutBackground)
        return

    ''' Inserts the userimage into the montage
    creates a empty image -> copies the cover image into the empty image
    applies the effects of the montage (effectFunct , resizeFunct, and the placementFunct)
    after the user image is placed -> places the front image
    '''

    def InsertUserImage(self, userImage):

        width, height = self.coverImage.size  # get the size of the first image in the layers
        self.userMontageImage = Image.new('RGBA', (width, height))  # create new empty image as blank canvas
        self.userMontageImage.paste(self.coverImage, (0, 0), self.coverImage)  # start by adding the initial image

        '''Function effectFunct
        add effect to the user image (ex: black and white filter)'''
        userImage = self.effectFunct(self.name, userImage)

        ''' 
        Function resizeFunct
        resizes the image to the to the value in settings (ex: Montagem1_Resize_x)'''
        userImage = self.resizeFunct(self.name, userImage)

        #TODO DEBUG MODE   remove in final function
        if settings["debug"]:
            userImage = ImageOps.expand(userImage, border=1, fill='red')  # add border to know the image position

        '''
        Function placementFunct
        Places the image in the position in the settings (ex: Montagem1_UserImage_x)'''
        self.userMontageImage = self.placementFunct(self.name, self.userMontageImage, userImage)

        self.userMontageImage.paste(self.frontImage, (0, 0), self.frontImage)  # paste front image
        return

    '''  Generates the postal with the user image
    creates and empty images
    pastes the postal image into the empty image
    resizes the user image to the intended size and pastes the user image into the postal'''

    def CreatePostalImage(self):

        width, height = self.postalImage.size  # get the size of the first image in the layers
        self.finalImage = Image.new('RGBA', (width, height))  # create new empty image as blank canvas
        self.finalImage = self.postalImage

        # TODO see size of userImage
        userImage_resize = resize(self.userMontageImage, 880, 1172)

        # TODO placement
        placement = (100, 65)
        self.finalImage.paste(userImage_resize, placement, userImage_resize)
        return
