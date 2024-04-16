import numpy as np
from PIL import ImageEnhance, Image, ImageOps

from Settings.SettingsHandler import settings


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

    A = np.matrix(matrix, dtype=float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)


def add_noise(image, intensity=0.1):
    """
    Add grain to the given image.

    :param image: PIL Image object
    :param intensity: Intensity of the grain (0 to 1)
    :return: PIL Image object with grain added
    """
    if intensity == 0:
        return image

    np_image = np.array(image)
    h, w, c = np_image.shape
    noise = np.random.normal(scale=intensity, size=(h, w, c))
    noisy_image = np.clip(np_image + noise * 255, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_image)


# function that retuns an image with the set size
def resize(image, size_x, size_y):
    size = size_x, size_y

    # imageResize = image.copy()
    # imageResize.thumbnail(size)

    imageResize = image.resize(size, resample=Image.BICUBIC)  # resize it

    return imageResize


def MontageBaseEffect(name, image):
    filter_brightness = ImageEnhance.Brightness(image)
    image = filter_brightness.enhance(settings[name + "_brightness"])
    # image = filter_brightness.enhance(settings["brightness"])

    filter_contrast = ImageEnhance.Contrast(image)
    image = filter_contrast.enhance(settings[name + "_contrast"])
    # image = filter_contrast.enhance(settings["contrast"])

    filter_sharpness = ImageEnhance.Sharpness(image)
    image = filter_sharpness.enhance(settings[name + "_sharpness"])
    # image = filter_sharpness.enhance(settings["sharpness"])

    filter_saturation = ImageEnhance.Color(image)
    image = filter_saturation.enhance(settings[name + "_saturation"])
    # image = filter_saturation.enhance(settings["saturation"])

    image = add_noise(image, intensity=settings[name + "_noise"])

    return image


def MontageColorizeEffect(name, image):
    image = MontageBaseEffect(name, image)

    r, g, b, alpha = image.split()  # We store the alpha , grayscale and colorize the image then put the alpha back
    image = image.convert('L')
    image = ImageOps.colorize(image, black="tan", white="bisque")
    image.putalpha(alpha)
    return image


def ColorizeEffect(name, image):
    r, g, b, alpha = image.split()  # We store the alpha , grayscale and colorize the image, he can then put back the alpha if we want to keep the transparent image
    image = image.convert('L')
    image = ImageOps.colorize(image, black=settings[name + "_colorize_black"], white=settings[name + "_colorize_white"])
    # image.putalpha(alpha)
    return image


def MontageNoEffect(name, image):
    return image


def MontageBasePlacement(name, coverImage, image):
    coverImage.paste(image, (settings[name + "_UserImage_x"], settings[name + "_UserImage_y"]), image)
    return coverImage


def MontageBaseResize(name, image):
    size = (settings[name + "_Resize_x"], settings[name + "_Resize_y"])
    resizedImage = image.resize(size)
    return resizedImage


def MontagePerspectiveTransformResize(name, image):
    image = MontageBaseResize(name, image)

    # image.save("in.png")
    width, height = image.size
    pa = [(0, 0), (width, 0), (width, height), (0, height)]  # Original image points

    TL = (0 + 300, 0 + 200)
    TR = (width , 0)
    BR = (width, height)
    BL = (0 + 300, height - 100)

    pb = [TL, TR, BR, BL]

    coeffs = find_coeffs(pb, pa)
    #image.save("in.png")
    image = image.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    #image.save("out.png")
    return image
