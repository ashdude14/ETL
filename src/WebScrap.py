import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Configuration
URL = "https://www.naukri.com/data-analyst-jobs"
Data_Set_path = "/app/data/data.csv"   #path inside the conatiner

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

def save_to_file(file, elements):
    """Save extracted data to the CSV file."""
    with open(file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for element in elements:
            text_content = element.text.strip().split('\n')
            formatted_row = [" | ".join(text_content)]
            writer.writerow(formatted_row)

def extract_and_save_data():
    """Extract and save data from the current page."""
    try:
        # Find data elements
        data_elements = driver.find_elements(By.CSS_SELECTOR, ".row1, .row2, .row3, .row4, .row5, .row6")
        save_to_file(Data_Set_path, data_elements)
    except Exception as e:
        print(f"Error during data extraction: {e}")

def close_popups():
    """Close any blocking pop-ups or overlays."""
    try:
        popup_close_button = driver.find_element(By.CSS_SELECTOR, ".styles_ppContainer__eeZyG .close-button")
        popup_close_button.click()
        print("Pop-up dismissed.")
    except NoSuchElementException:
        print("No pop-up to close.")

try:
    driver.get(URL)
    time.sleep(3)  # Allow the page to load

    # Initialize CSV with headers (optional)
    with open(Data_Set_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Job Details"])  # Add headers if needed

    while True:
        # Extract and save data from the current page
        extract_and_save_data()

        try:
            # Handle any pop-ups
            close_popups()

            # Locate the "Next" button
            next_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/.."))
            )

            # Scroll to and click the "Next" button
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            driver.execute_script("arguments[0].click();", next_button)

            # Wait for the next page to load
            time.sleep(3)

        except TimeoutException:
            print("No more pages to navigate.")
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()