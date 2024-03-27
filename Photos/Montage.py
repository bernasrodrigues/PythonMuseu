import glob
import os

import rembg
import numpy as np
from PIL import Image


# A Montage contains the list of layers that compose an Image
# the user images is inserted in the position that we want it to be


class Montage:

    def __init__(self, folder):
        self.name = folder  # Name for the montage
        self.coverImage = None  # Original image
        self.frontImage = None  # Image in front of the user
        self.exampleImage = None  # Image of the user
        self.finalImage = None  # Final generated image

        self.imageProcessing = None
        self.ApplyEffects = None

        print(f"Creating Montage for {folder}")

        currentDirectory = os.path.dirname(os.path.abspath(__file__))
        currentDirectory = os.path.join(currentDirectory, folder)
        allFilesInDir = [os.path.join(currentDirectory, file_name) for file_name in os.listdir(currentDirectory) if
                         os.path.isfile(os.path.join(currentDirectory, file_name))]

        for fileName in allFilesInDir:
            imageName = os.path.basename(fileName)  # Check layer name

            if os.path.basename(fileName) == "cover.png":  # add cover image
                self.coverImage = Image.open(fileName).convert('RGBA')
                print(f"Image {imageName} added as cover")

            elif os.path.basename(fileName) == "topo.png":  # add front image
                self.frontImage = Image.open(fileName).convert('RGBA')
                print(f"Image {imageName} added as front image")

            elif os.path.basename(fileName) == "user.png":  # add example image
                self.exampleImage = Image.open(fileName).convert('RGBA')
                print(f"Image {imageName} added as example image")  # leave space for the user image

        print(f"Montage {folder} created\n---------------------")

    def GetCoverImage(self):
        return self.coverImage

    # User image -> file path to the user image
    def CreateFinalImage(self, userImage):
        # Apply background removal using rembg
        userImageWithoutBackground = rembg.remove(userImage)
        self.InsertUserImage(userImageWithoutBackground)


    # User Image -> image with the recorted background
    def InsertUserImage(self, userImage):

        width, height = self.coverImage.size  # get the size of the first image in the layers
        self.finalImage = Image.new('RGBA', (width, height))  # create new empty image as blank canvas

        self.finalImage.paste(self.coverImage, (0, 0), self.coverImage)
        self.finalImage.paste(userImage, (0, 0), userImage)
        self.finalImage.paste(self.frontImage, (0, 0), self.frontImage)

