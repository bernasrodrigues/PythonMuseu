import os

import rembg
from PIL import Image, ImageOps

from Settings.SettingsHandler import settings


# A Montage contains the list of layers that compose an Image
# the user images is inserted in the position that we want it to be


class Montage:

    def __init__(self, folder, placementFunct, effectFunct):
        self.name = folder  # Name for the montage
        self.coverImage = None  # Original image
        self.frontImage = None  # Image in front of the user
        self.exampleImage = None  # Image of the user
        self.userMontageImage = None  # Final generated image
        self.postalImage = None     # image of the postal
        self.finalImage = None      # final image on the postal

        # functions to apply Effects
        self.placementFunct = placementFunct
        self.effectFunct = effectFunct

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

    # User image -> file path to the user image
    def createUserMontageImage(self, userImage):
        # Apply background removal using rembg
        userImageWithoutBackground = rembg.remove(userImage)
        self.InsertUserImage(userImageWithoutBackground)

    # User Image -> image with the recorted background
    def InsertUserImage(self, userImage):

        width, height = self.coverImage.size  # get the size of the first image in the layers
        self.userMontageImage = Image.new('RGBA', (width, height))  # create new empty image as blank canvas

        userImage = self.effectFunct(self.name, userImage)  # add effect to the user image (ex: black and white filter)

        # TODO remove this
        userImage = ImageOps.expand(userImage, border=1, fill='red')  # add border to know the image position

        self.userMontageImage.paste(self.coverImage, (0, 0), self.coverImage)  # start by adding the initial image

        self.userMontageImage = self.placementFunct(self.name,
                                                    self.userMontageImage,
                                                    userImage)  # paste user image

        self.userMontageImage.paste(self.frontImage, (0, 0), self.frontImage)  # paste front image

    def CreatePostalImage(self):

        width, height = self.postalImage.size  # get the size of the first image in the layers
        self.finalImage = Image.new('RGBA', (width, height))  # create new empty image as blank canvas
        self.finalImage = self.postalImage
        self.finalImage.paste(self.userMontageImage, (0, 0), self.userMontageImage)
