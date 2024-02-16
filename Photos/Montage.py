import glob
import os

import rembg
import numpy as np
from PIL import Image


# A Montage contains the list of layers that compose an Image
# the user images is inserted in the position that we want it to be


class Montage:

    def __init__(self, folder, userImageLayer):
        self.name = folder  # Name for the montage
        self.coverImage = None
        self.layers = {}  # List of the image locations that compose the montage
        self.userImageLayer = userImageLayer  # Indicates what layer the user images is supposed to be in

        print(f"Creating Montage {folder}")

        currentDirectory = os.path.dirname(os.path.abspath(__file__))
        currentDirectory = os.path.join(currentDirectory, folder)
        allFilesInDir = [os.path.join(currentDirectory, file_name) for file_name in os.listdir(currentDirectory) if
                         os.path.isfile(os.path.join(currentDirectory, file_name))]

        index = 0
        for fileName in allFilesInDir:

            imageName = os.path.basename(fileName)  # Check layer name

            if os.path.basename(fileName) == "cover.png":  # add cover image
                self.coverImage = Image.open(fileName).convert('RGBA')
                print(f"Image {imageName} added as cover")  # leave space for the user image
                continue

            if index == userImageLayer:
                self.layers[index] = None
                print(f"Left space for user image in layer: {index}")
                index += 1
                self.layers[index] = Image.open(fileName).convert('RGBA')
                print(f"Image {imageName} added in layer: {index}")
                index += 1
            else:
                self.layers[index] = Image.open(fileName).convert('RGBA')
                print(f"Image {imageName} added in layer: {index}")
                index += 1

        # Edge case to prevent situations where the user image is on the last layer
        if index == userImageLayer:
            self.layers[index] = None
            print(f"Left space for user image in layer: {index}")

        self.finalImage = None

        # self.finalImage = self.layers[0]
        # print(self.layers)
        #
        #
        # for layer in self.layers.values():
        #     self.finalImage.paste(layer, (0, 0), layer)
        #
        # self.finalImage.save(self.name + "_finalImage.png")
        # print(f"Final image saved to {self.name}_finalImage.png")
        print(f"Montage {folder} created\n---------------------")

    def GetCoverImage(self):

        return self.coverImage

    # User image -> file path to the user image
    def InsertUserImage(self, userImage):

        # input_image = Image.open(userImage)

        # Convert the input image to a numpy array
        # input_array = np.array(userImage)

        # Apply background removal using rembg
        imageWithoutBackground = rembg.remove(userImage)
        # imageWithoutBackground = userImage


        # Create a PIL Image from the output array  (user image with the background removed)
        # recortedImage = Image.fromarray(output_array)

        self.CreateFinalImage(imageWithoutBackground)

    # User Image -> image with the recorted background
    def CreateFinalImage(self, userImage):

        #self.finalImage = userImage

        self.layers[self.userImageLayer] = userImage
        # self.finalImage = self.layers[0]

        width, height = self.layers[0].size  # get the size of the first image in the layers
        self.finalImage = Image.new('RGBA', (width, height))  # create new empty image as blank canvas

        for layer in self.layers.values():  # for each layer paste the image unto the canvas
            self.finalImage.paste(layer, (0, 0), layer)

        # self.finalImage.save(self.name + "_finalImage.png")
        # print(f"Final image saved to {self.name}_finalImage.png")

    def InsertUserImage2(self, userImage):

        # Apply background removal using rembg
        output_array = rembg.remove(userImage)

        # Create a PIL Image from the output array  (user image with the background removed)
        recortedImage = Image.fromarray(output_array)
        return recortedImage
        # self.CreateFinalImage(recortedImage)

    def CreateFinalImage2(self, userImage):

        self.layers[self.userImageLayer] = userImage
        # self.finalImage = self.layers[0]
        width, height = self.layers[0].size  # get the size of the first image in the layers
        self.finalImage = Image.new('RGB', (width, height))  # create new empty image as blank canvas

        for layer in self.layers.values():
            self.finalImage.paste(layer, (0, 0), layer)

        logo = Image.open("../_OLD/Logo.png")
        self.finalImage.paste(logo, (0, 0), logo)

        self.finalImage.save(self.name + "_finalImage.png")
        return self.finalImage
        # print(f"Final image saved to {self.name}_finalImage.png")
