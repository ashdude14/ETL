from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
import time
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Constants
URL = "https://www.naukri.com/data-analyst-jobs"
DATA_SET_PATH = "/app/data/data.csv"

def test_server():
    """Check if the Selenium server is available."""
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get("http://standaloneETL:4444/wd/hub")
        if response.status_code == 200:
            logging.info("Selenium server is available and ready.")
        else:
            logging.warning(f"Selenium server responded with status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error checking Selenium server availability: {e}")
        raise

def ensure_directory_exists(file_path):
    """Ensure the directory for the file path exists."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def save_to_file(file, elements):
    """Save extracted data to the CSV file."""
    try:
        with open(file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for element in elements:
                text_content = element.text.strip().split('\n')
                formatted_row = [" | ".join(text_content)]
                writer.writerow(formatted_row)
        logging.info(f"Saved {len(elements)} records to {file}.")
    except Exception as e:
        logging.error(f"Error saving data to file: {e}")

def extract_and_save_data(driver):
    """Extract job details from the page and save them to the file."""
    try:
        data_elements = driver.find_elements(By.CSS_SELECTOR, ".row1, .row2, .row3, .row4, .row5, .row6")
        save_to_file(DATA_SET_PATH, data_elements)
    except NoSuchElementException as e:
        logging.warning(f"No data elements found: {e}")
    except Exception as e:
        logging.error(f"Error during data extraction: {e}")

def scrap(url, file_path):
    """Scrape job details from the given URL."""
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Ensure the output directory exists
    ensure_directory_exists(file_path)

    # Initialize the WebDriver
    try:
        driver = webdriver.Remote(command_executor='http://standaloneETL:4444/wd/hub', options=chrome_options)
        logging.info("WebDriver initialized.")
    except WebDriverException as e:
        logging.error(f"Failed to initialize WebDriver: {e}")
        return

    try:
        driver.get(url)
        logging.info(f"Accessed URL: {url}")
        time.sleep(5)  # Wait for the page to load

        # Write the header to the CSV file
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Job Details"])  # Add headers

        # Loop through pages and scrape data
        while True:
            extract_and_save_data(driver)
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/.."))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                driver.execute_script("arguments[0].click();", next_button)
                logging.info("Navigated to the next page.")
                time.sleep(5)  # Wait for the next page to load
            except TimeoutException:
                logging.info("No more pages to navigate.")
                break
    except Exception as e:
        logging.error(f"An error occurred during scraping: {e}")
    finally:
        driver.quit()
        logging.info("WebDriver session ended.")

if __name__ == "__main__":
    try:
        test_server()
        scrap(URL, DATA_SET_PATH)
    except Exception as e:
        logging.error(f"Script failed with an error: {e}")
