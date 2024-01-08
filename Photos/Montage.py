import rembg
import numpy as np
from PIL import Image


# A Montage contains the list of layers that compose an Image
# the user images is inserted in the position that we want it to be


class Montage:

    def __init__(self, name, layersList, userImageLayer):
        self.name = name  # Name for the montage
        self.layers = {}  # List of the image locations that compose the montage
        self.userImageLayer = userImageLayer  # Indicates what layer the user images is supposed to be in

        for index, layer in enumerate(layersList):

            if index == userImageLayer:
                self.layers[index] = None
                pass

            input_image = Image.open(layer)
            self.layers[index] = input_image

        self.finalImage = None

    def InsertUserImage(self, userImage):
        input_image = Image.open(userImage)

        # Convert the input image to a numpy array
        input_array = np.array(input_image)

        # Apply background removal using rembg
        output_array = rembg.remove(input_array)

        # Create a PIL Image from the output array  (user image with the background removed)
        recortedImage = Image.fromarray(output_array)

        self.HandleLayers(recortedImage)

    def HandleLayers(self, userImage):
        print("")

        self.layers[self.userImageLayer] = userImage

        self.finalImage = self.layers[0].copy()

        for layer in self.layers.values():
            self.finalImage.paste(layer, (0, 0), layer)

        self.finalImage.save(self.name + "_finalImage.png")
        print(f"Final image saved to {self.name}_finalImage.png")
