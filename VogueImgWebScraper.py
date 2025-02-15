import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup

# -------------------------------
# Helper Function for Login Input
# -------------------------------
def send_keys_safe(driver, by, value, text, wait_time=10, retries=5):
    """Attempts to locate an element and send keys. Retries if needed."""
    for attempt in range(retries):
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.element_to_be_clickable((by, value))
            )
            element.clear()
            element.send_keys(text + Keys.ENTER)
            return True
        except (StaleElementReferenceException, TimeoutException) as e:
            print(f"Attempt {attempt+1}: Issue encountered ({e}). Retrying...")
            time.sleep(1)
    return False

# -------------------------------
# Setup and Login Process
# -------------------------------

# Set up ChromeDriver service
service = Service(executable_path="./chromedriver")  # Update with correct path
driver = webdriver.Chrome(service=service)

# Open Vogue login page
login_url = ("https://id.condenast.com/interaction/T_j9KslhPJhIfigHqfFHB/email"
             "?_sp=b7cc4e55-152d-4cdd-9be2-521e0c9abd93.1738423524782"
             "&xid=1ccb2ef8-4457-4d5e-800d-135c819bb294"
             "&scope=openid%20offline_access"
             "&state=%7B%22redirectURL%22%3A%22%2F%3F_sp%3Db7cc4e55-152d-4cdd-9be2-521e0c9abd93.1738423524782%22%7D"
             "&prompt=select_account%20consent"
             "&source=VERSO_NAVIGATION"
             "&client_id=condenast.identity.fbc9096dc61f9b79c5ac4c85998da075"
             "&redirect_uri=https%3A%2F%2Fwww.vogue.com%2Fauth%2Fcomplete"
             "&response_type=code")
driver.get(login_url)

# Wait for email input field
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "text-field__input"))
)

# Step 1: Enter Email
if send_keys_safe(driver, By.CLASS_NAME, "text-field__input", "reddy_bhavya@icloud.com"):
    print("Email entered successfully.")
else:
    print("Failed to enter email.")

# Wait before entering password
time.sleep(2)

# Step 2: Enter Password
if send_keys_safe(driver, By.CLASS_NAME, "text-field__input", "VF4J8tiHx3Ldc"):
    print("Password entered successfully.")
else:
    print("Failed to enter password.")

# Allow login to complete
time.sleep(5)

# -------------------------------
# Navigate to Target Slideshow Page
# -------------------------------
target_url = "https://www.vogue.com/fashion-shows/spring-2025-couture/jean-paul-gaultier?_sp=b7cc4e55-152d-4cdd-9be2-521e0c9abd93.1738439072162"
driver.get(target_url)

# Wait for page to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)
print("Navigated to slideshow page.")

# -------------------------------
# Click "Load More" Until All Images Are Loaded
# -------------------------------
while True:
    try:
        # Locate the "Load More" button
        load_more_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Load More')]"))
        )

        # Scroll into view to avoid interception
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_button)
        time.sleep(1)  # Small pause to let page settle

        # Try clicking normally
        try:
            load_more_button.click()
            print("Clicked 'Load More' button.")
        except ElementClickInterceptedException:
            print("Click intercepted. Using JavaScript click.")
            driver.execute_script("arguments[0].click();", load_more_button)

        time.sleep(3)  # Wait for images to load

    except (TimeoutException, NoSuchElementException):
        print("No more 'Load More' button found. All images should be loaded.")
        break

# -------------------------------
# Extract Image URLs
# -------------------------------
soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract Image URLs
image_divs = soup.find_all("div", class_="GridItem-buujkM dEqBaI grid--item")
image_urls = [
    div.find("img", class_="ResponsiveImageContainer-eybHBd fptoWY responsive-image__image")["src"]
    for div in image_divs if div.find("img")
]

# -------------------------------
# Download Images
# -------------------------------
os.makedirs("vogue_images", exist_ok=True)

for idx, img_url in enumerate(image_urls):
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            image_path = os.path.join("vogue_images", f"image_{idx+1}.jpg")
            with open(image_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {image_path}")
        else:
            print(f"Failed to download {img_url}")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

# -------------------------------
# Cleanup
# -------------------------------
time.sleep(5)
driver.quit()
print("All images downloaded. Script completed.")