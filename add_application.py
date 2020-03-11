"""
Creates an application to generate screenshots for the Getting Started Guide
"""

from selenium import webdriver
from time import sleep
import re
import config as cfg
import process_image as pi
import helpers

# Get device listings from device-types endpoint
device_config = helpers.get_device_listings()

# Setup webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.executable_path = "./chromedriver"
driver = webdriver.Chrome(options=options)

# Use implicit waits
driver.implicitly_wait(5)

# This is hacky but needed to get the device list dropdown to fit on the screen
# TODO look into using a key down to loop through these instead
driver.set_window_size(5000, 5000)
driver.maximize_window()

# Choose the right starting point
if cfg.staging == True:
    driver.get(cfg.balena_cloud_staging_url)
else:
    driver.get(cfg.balena_cloud_url)

driver.save_screenshot("./screenshots/steps/1-login-page.png")

# Fill username and password
username = driver.find_element_by_id("root_username")
password = driver.find_element_by_id("root_password")

# Save to env vars
username.send_keys(cfg.username)
password.send_keys(cfg.password)

# Click the login button
driver.find_element_by_xpath("//button[@type='submit']").click()
driver.save_screenshot("./screenshots/steps/2-logged-in.png")

# Close the modal
driver.find_element_by_xpath("//body[@id='dashboard__applications']/div[4]/div/div/div[2]/div/div[2]/button").click()
print("Closed the modal")
driver.save_screenshot("./screenshots/steps/3-closed-modal.png")

# Close the banner to have a clean homepage
driver.find_element_by_css_selector(".fa-times > path").click()
driver.save_screenshot("./screenshots/steps/4-close-banner.png")
print("Closed the banner")

# Devices are indexed from 1
x = 1

while True:
    try:
        print("Create Application " + str(x))

        # Clean exsting screenshots
        helpers.clean_screenshots()

        # Click the Create Application button
        driver.find_element_by_xpath('//button/div').click()
        driver.save_screenshot("./screenshots/steps/5-create-application.png")

        # Expand the devices dropdown 
        # TODO determine how many devices in this list so we can loop properly and provide progress
        driver.find_element_by_xpath('//*[@id="e2e-new-app-device-type-list"]').click()

        # Extract the device name and format for consistency
        device = driver.find_element_by_xpath(
            '//*[@id="e2e-new-app-device-type-list__select-drop"]/div[2]/div[' + str(x) + ']/button/div/div').text
        device = re.sub(r'\([^)]*\)', '', device)
        device = device.replace(" ", "")
        print("Creating: " + device_config[device])

        # Select the device
        driver.find_element_by_xpath(
            '//*[@id="e2e-new-app-device-type-list__select-drop"]/div[2]/div[' + str(x) + ']/button/div/div').click()
        driver.save_screenshot("./screenshots/steps/6-select-device.png")

        # Set the application to starter
        driver.find_element_by_xpath("//button[@id='newAppApplicationType']/div/div/div/div").click()
        driver.find_element_by_xpath(
            "//div[@id='newAppApplicationType__select-drop']/div/div[3]/button/div/div").click()
        driver.save_screenshot("./screenshots/steps/7-select-starter.png")

        # Fill out the application name
        app_name_field = driver.find_element_by_xpath('//*[@id="e2e-application-name-input"]')
        app_name = "First-App" + "-" + device  # make sure less than 30 chars
        app_name = re.sub('[^A-Za-z0-9-_]+', '', app_name) # have to remove all special characters
        app_name = (app_name[:29] + '-') if len(app_name) > 30 else app_name
        app_name_field.send_keys(app_name)
        driver.save_screenshot("./screenshots/steps/8-enter-application-name.png")

        # Adjust window size to take screenshots
        driver.set_window_size(1366, 768)

        # Take the create application screenshot
        driver.save_screenshot("./screenshots/create_application/" + device_config[device] + ".png")

        # Create Application
        driver.find_element_by_xpath("//button[contains(.,'Create new application')]").click()
        driver.save_screenshot("./screenshots/steps/8-2-click-add-new application.png")
        print("Waiting for application to be created")
        sleep(60)

        # Take the application screenshot
        driver.save_screenshot("./screenshots/application/" + device_config[device] + ".png")

        # Add a device
        print("Add a device")
        driver.find_element_by_xpath("//button[contains(.,'Add device')]").click()
        driver.save_screenshot("./screenshots/steps/9-click-add-device.png")

        # Expand the options on add device page
        driver.find_element_by_css_selector(".sc-gZMcBi > .StyledBox-sc-13pk1d4-0 path").click()
        driver.save_screenshot("./screenshots/steps/10-expand-options.png")

        # Take the device screenshot
        driver.save_screenshot("./screenshots/devices/" + device_config[device] + ".png")

        # Close the device window
        driver.find_element_by_css_selector(".sc-bZQynM > svg > g > path").click()
        driver.save_screenshot("./screenshots/steps/11-close-device-window.png")

        # Delete the application
        print("Now delete the application")

        # Click the Actions button
        driver.find_element_by_xpath(
            "//body[@id='dashboard__application__devices']/div/div/dashboard/div/div/div/div/ul/li[8]/a/div/i").click()
        driver.save_screenshot("./screenshots/steps/12-click-actions.png")

        # Click delete application button
        driver.find_element_by_xpath("//button[contains(.,'Delete this application…')]").click()
        driver.save_screenshot("./screenshots/steps/13-click-delete-application.png")

        # Find and fill the delete application confirmation
        name = driver.find_element_by_css_selector(".e2e-name-confirmation-input")
        name.send_keys(app_name)
        driver.save_screenshot("./screenshots/steps/14-confirm-delete-application.png")
        driver.find_element_by_css_selector(".e2e-name-confirmation-submit-button").click()

        # Wait for the application to be deleted before moving on
        print("Application deleted")
        sleep(60)

        # Finally format the image for the documentation
        pi.format_create_application_image(device_config[device])
        pi.format_device_application(device_config[device])
        pi.format_add_new_device(device_config[device])

        # Output the completed device and move onto the next one
        print(device_config[device] + " Completed")
        driver.set_window_size(5000, 5000)
        x += 1

    except Exception as e:
        # "If we get here we have probably run out of devices."
        print(e)
        break
        
# Complete
print("End")
driver.close()
