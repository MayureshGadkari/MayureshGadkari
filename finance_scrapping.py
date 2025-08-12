from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Setup Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Open Finviz login page
driver.get("https://finviz.com/login.ashx")
time.sleep(2)

# Create ActionChains instance
actions = ActionChains(driver)

# Find the email input field
username = driver.find_element(By.NAME, "email")
# Move to email field and click
actions.move_to_element(username).pause(0.5).click().perform()
time.sleep(1)
username.send_keys("mayuresh.gadkari_19@sakec.ac.in")

# Find the password input field
password = driver.find_element(By.NAME, "password")
# Move to password field and click
actions.move_to_element(password).pause(0.5).click().perform()
time.sleep(1)
password.send_keys("Password@1234567890")

# Submit form (press Enter)
password.send_keys(Keys.RETURN)
time.sleep(3)

# (Optional) Navigate to screener page after login
driver.get("https://finviz.com/screener.ashx?v=111")
time.sleep(3)

all_data = []
headers = []

# Step 3: Loop through all pages
while True:
    time.sleep(2)

    # Locate the table
    table = driver.find_element(By.XPATH, '//*[@id="screener-table"]')
    rows = table.find_elements(By.TAG_NAME, "tr")

    # Step 4: Extract headers only once
    if not headers:
        headers = ['No.', 'Ticker', 'Company', 'Sector', 'Industry', 'Country', 'Market Cap', 'P/E', 'Price', 'Change',
                   'Volume']
        #headers = [th.text for th in rows[0].find_elements(By.TAG_NAME, "td")][:11]  # Limit to actual columns
        #headers = [th.text for th in rows[0].find_elements(By.TAG_NAME, "td")]

    # Step 5: Extract row data
    for row in rows[1:]:
        cols = [col.text for col in row.find_elements(By.TAG_NAME, "td")]
        if cols:
            all_data.append(cols)

    # Step 6: Check for next page button
    try:
        next_button = driver.find_element(By.LINK_TEXT, "next")
        next_button.click()
    except:
        break  # No more pages

# Step 7: Save to Excel using pandas
df = pd.DataFrame(all_data, columns=headers)
df.to_excel("finviz_stock_data.xlsx", index=False)
print("✅ Scraping complete. Data saved to 'finviz_stock_data.xlsx'.")


driver.quit()