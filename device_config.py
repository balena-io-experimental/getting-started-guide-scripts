"""
Script to create the device dictionary
Can exclude boards from the docs by adding to the config file
"""

import requests
import json
import config

# Get device listings from device-types endpoint
response = requests.get("https://api.balena-cloud.com/device-types/v1/")
devices = response.json()

device_logo = "/img/device/"

device_config = []

for device in devices:

    # Determine community supported board
    if "community" in device:
        community = True
        # print(device["name"])
    else:
        community = False

    # Determine if there are instructions
    if "instructions" in device:

        instructions = []

        for i in device["instructions"]:
            instructions.append({"i": i})
    else:
        instructions = ""

    # try to guess the boot media
    if "eMMC" in str(instructions):
        bootMedia = "eMMC"
    elif "USB" in str(instructions):
        bootMedia = "USB key"
    else:
        bootMedia = "SD card"

    # try to guess the boot media
    if "Etcher" in str(instructions):
        etcher = True
    else:
        etcher = False

    # exclude some boards
    if device["slug"] in config.exclude:
        pass
    else:
        device_config.append(
            {
                "id": device["slug"],
                "name": str.strip(device["name"].replace('(EXPERIMENTAL)', '').replace('(DISCONTINUED)', '').replace('(NEW)', '')),
                "arch": device["arch"],
                "bootMedia": bootMedia,
                "state": device["state"],
                "machine": device["yocto"]["machine"],
                "community": community,
                "icon": "/img/device/" + device['slug'] + ".svg",
                "instructions": instructions,
                "etcher": etcher
            }
    )

device_config = sorted(device_config, key=lambda k: k['name'])

# Filter supported boards as we don't want to output discontinued ones
supported = [v for v in device_config if v["state"] != "DISCONTINUED" and v["name"] != "Generic"]

with open("./output/device-dict.json", "w") as f:
        json.dump(supported, f, indent=4)
