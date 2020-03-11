"""
Processes the images to crop for docs
"""

from PIL import Image
import os


def format_create_application_image(device):
    """
    Format the create application image to the correct size
    """
    img = Image.open("./screenshots/create_application/" + device + ".png")
    left = 666
    top = 350
    right = 2065
    bottom = 1200
    cropped_img = img.crop((left, top, right, bottom))
    cropped_img.save(
        "./screenshots/create_application/edited/" + device + ".png")


def format_device_application(device):
    """
    Format the device application to the correct size
    """
    img = Image.open("./screenshots/application/" + device + ".png")
    left = 0
    top = 120
    right = 2712
    bottom = 668
    cropped_img = img.crop((left, top, right, bottom))
    cropped_img.save("./screenshots/application/edited/" + device + ".png")


def format_add_new_device(device):
    """
    Format the add device image to the correct size
    """
    # If want to crop out the instructions set the right to 1366 (orig 2712)
    # If want to crop out network connection and below set bottom to 850 (orig 1505)
    img = Image.open("./screenshots/devices/" + device + ".png")
    left = 75
    top = 75
    right = 1390
    bottom = 1020
    cropped_img = img.crop((left, top, right, bottom))
    cropped_img.save("./screenshots/devices/edited/" + device + ".png")


def format_cli_release():
    """
    Format the CLI release image
    """
    img = Image.open("./screenshots/cli/cli-release.png")
    left = 400
    top = 550
    right = 2400
    bottom = 1450
    cropped_img = img.crop((left, top, right, bottom))
    cropped_img.save("./screenshots/cli/cli-release.png")


def format_standalone_images():
    """
    Standalone image editing
    """
    for filename in os.listdir("./screenshots/devices/"):
        # Strip the extension
        if filename.endswith(".png"):
          filename = os.path.splitext(filename)[0]
          format_create_application_image(filename)
          format_device_application(filename)
          format_add_new_device(filename)


if __name__ == "__main__":
    format_standalone_images()
    print("Done")
