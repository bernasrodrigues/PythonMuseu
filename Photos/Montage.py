import glob
import rembg
import numpy as np
from PIL import Image


# A Montage contains the list of layers that compose an Image
# the user images is inserted in the position that we want it to be


class Montage:

    # def __init__(self, name, layersList, userImageLayer):
    #     self.name = name  # Name for the montage
    #     self.layers = {}  # List of the image locations that compose the montage
    #     self.userImageLayer = userImageLayer  # Indicates what layer the user images is supposed to be in
    #
    #     for index, layer in enumerate(layersList):
    #
    #         if index == userImageLayer:
    #             self.layers[index] = None
    #             pass
    #
    #         input_image = Image.open(layer)
    #         self.layers[index] = input_image
    #
    #     self.finalImage = None

    def __init__(self, name, folder, userImageLayer):
        self.name = name  # Name for the montage
        self.layers = {}  # List of the image locations that compose the montage
        self.userImageLayer = userImageLayer  # Indicates what layer the user images is supposed to be in

        folderImages = glob.glob(folder + "/*.png")
        for index, layer in enumerate(folderImages):

            print(layer)
            if index == userImageLayer:
                self.layers[index] = None
                index += 1
                self.layers[index] = Image.open(layer)
            else:
                self.layers[index] = Image.open(layer)

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

    # User image -> file path to the user image
    def InsertUserImage(self, userImage):
        input_image = Image.open(userImage)

        # Convert the input image to a numpy array
        input_array = np.array(input_image)

        # Apply background removal using rembg
        output_array = rembg.remove(input_array)

        # Create a PIL Image from the output array  (user image with the background removed)
        recortedImage = Image.fromarray(output_array)

        self.CreateFinalImage(recortedImage)

    # User Image -> image with the recorted background
    def CreateFinalImage(self, userImage):

        self.layers[self.userImageLayer] = userImage
        # self.finalImage = self.layers[0]

        width, height = self.layers[0].size                     # get the size of the first image in the layers
        self.finalImage = Image.new('RGB', (width, height))     # create new empty image as blank canvas

        for layer in self.layers.values():  # for each layer paste the image unto the canvas
            self.finalImage.paste(layer, (0, 0), layer)

        self.finalImage.save(self.name + "_finalImage.png")
        print(f"Final image saved to {self.name}_finalImage.png")

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
        self.finalImage = Image.new('RGB', (500, 500))

        for layer in self.layers.values():
            self.finalImage.paste(layer, (0, 0), layer)

        self.finalImage.save(self.name + "_finalImage.png")
        return self.finalImage
        # print(f"Final image saved to {self.name}_finalImage.png")
