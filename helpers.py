import requests
import re
import json
import os
import glob


def get_device_listings():
    """
    Get the device listings that we need to use as a dictionary
    """
    response = requests.get("https://api.balena-cloud.com/device-types/v1/")
    devices = response.json()

    device_config = {}

    for device in devices:
        d = re.sub(r'\([^)]*\)', '', device['name'])
        d = d.replace(" ", "")

        if device["slug"] != "raspberrypi3-64":
            device_config[d] = device["slug"]

    # Save this to a file for review
    with open("./output/devices.json", "w") as f:
        json.dump(device_config, f, indent=4)

    return device_config


def clean_screenshots():
    """
    Delete the tmp screenshots so we know if we fail
    """
    tmp_screenshots = glob.glob("./screenshots/steps/*.png")
    for f in tmp_screenshots:
        os.remove(f)
