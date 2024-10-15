from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

def main():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": os.path.join(os.getcwd(), "downloads"),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })

    # Set up the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the page
        driver.get("https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/consumer-price-index-australia/jun-quarter-2024")

        # Wait for the page to load completely
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Wait a bit more to ensure dynamic content is loaded
        time.sleep(5)

        # Find all buttons with the specific class
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.chart-export.chart-export-csv.chart-export-buttons")

        print(buttons)
        # Look for the button with the specific aria-label
        target_button = None
        for button in buttons:
            if button.get_attribute("aria-label") == "All groups CPI and Trimmed mean, Australia, annual movement (%).csv":
                target_button = button
                break

        if target_button:
            # Click the button
            driver.execute_script("arguments[0].click();", target_button)
            print("Download button clicked. Check your downloads folder.")
            
            # Wait for the download to complete (adjust the sleep time if needed)
            time.sleep(10)
        else:
            print("Could not find the specific download button.")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
