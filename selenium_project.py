from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from openpyxl import Workbook

# Setup Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open target website
driver.get("http://quotes.toscrape.com")
time.sleep(2)  # wait for page to load

# Scrape quotes and authors
quotes = driver.find_elements(By.CLASS_NAME, "quote")

# Prepare Excel workbook
wb = Workbook()
ws = wb.active
ws.title = "Quotes"
ws.append(["Quote", "Author"])  # Header row

for quote in quotes:
    text = quote.find_element(By.CLASS_NAME, "text").text
    author = quote.find_element(By.CLASS_NAME, "author").text
    ws.append([text, author])  # Append data row

# Save the workbook
wb.save("quotes.xlsx")
print("Data saved to quotes.xlsx")

# Close the browser
driver.quit()

