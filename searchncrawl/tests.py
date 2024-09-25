from django.test import TestCase
import os

# Create your tests here.


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

current_path = os.path.dirname(os.path.abspath(__file__))
CHROME_DRIVER_PATH = os.path.join(current_path, 'chromedriver-mac-arm64', 'chromedriver')

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("--no-sandbox")  # Required for some server environments
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")

# Path to ChromeDriver if not in PATH
# driver = webdriver.Chrome(executable_path='/path/to/chromedriver', options=chrome_options)

# If chromedriver is in PATH:
driver = webdriver.Chrome(options=chrome_options)

# Example: Opening a webpage
search_url = "https://www.google.com/search?q=screen&tbm=shop"
driver.get(search_url)
print(driver.title)

driver.quit()
