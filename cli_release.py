"""
Creates screenshot of latest CLI GitHub release
"""

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import process_image

# Setup webdriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.executable_path = "./chromedriver"
driver = webdriver.Chrome(options=options)

# Use implicit waits
driver.implicitly_wait(5)

driver.set_window_size(1366, 768)

driver.get("https://github.com/balena-io/balena-cli/releases")

# Close the preview
driver.find_element_by_css_selector('.js-signup-prompt-button').click()

# Find the latest release
element = driver.find_element_by_class_name('label-latest')
actions = ActionChains(driver)
actions.move_to_element(element).perform()

# Save the screenshot and process
driver.save_screenshot("./screenshots/cli/cli-release.png")
process_image.format_cli_release()

print("Done")
