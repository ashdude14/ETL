from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os

# Check if CHROME_BIN environment variable is set or fallback to default
chrome_bin = os.environ.get("CHROME_BIN", "/usr/bin/chromium")

# Create ChromeOptions instance
chrome_options = Options()

# Set the binary location for Chrome or Chromium
chrome_options.binary_location = chrome_bin

# Add headless argument for running without a GUI
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Path to chromedriver (it should match your Chrome/Chromium version)
chromedriver_path = "/usr/bin/chromedriver"  # Ensure this path is correct

# Create the Service object for ChromeDriver
service = Service(executable_path=chromedriver_path)

# Initialize the WebDriver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Now you can use the driver to navigate and interact with the web page
driver.implicitly_wait(5)
driver.get("https://docs.docker.com/compose/")


# Do something with the driver...
print(driver.title)


# Always quit the driver at the end
driver.quit()