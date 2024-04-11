from PIL import ImageEnhance, ImageTk

from Settings.SettingsHandler import settings


# function that retuns an image with the set size
def resize(image, size_x, size_y):
    size = size_x, size_y

    imageResize = image.copy()
    imageResize.thumbnail(size)

    return imageResize


def MontageBaseEffect(name, image):
    filter_brightness = ImageEnhance.Brightness(image)
    image = filter_brightness.enhance(settings[name + "_brightness"])
    #image = filter_brightness.enhance(settings["brightness"])

    filter_contrast = ImageEnhance.Contrast(image)
    image = filter_contrast.enhance(settings[name + "_contrast"])
    #image = filter_contrast.enhance(settings["contrast"])

    filter_sharpness = ImageEnhance.Sharpness(image)
    image = filter_sharpness.enhance(settings[name + "_sharpness"])
    #image = filter_sharpness.enhance(settings["sharpness"])

    filter_saturation = ImageEnhance.Color(image)
    image = filter_saturation.enhance(settings[name + "_saturation"])
    #image = filter_saturation.enhance(settings["saturation"])

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
