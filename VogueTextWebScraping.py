from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from bs4 import BeautifulSoup
import time

# -------------------------------
# Helper functions for login input
# -------------------------------
def send_keys_safe(driver, by, value, text, wait_time=10, retries=5):
    """
    Attempts to locate an element and send keys to it.
    If a stale element exception occurs, it retries a few times.
    """
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

# Set up the ChromeDriver service with the correct executable path
service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

# Open the Condé Nast/Vogue login page
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

# Wait for the first input field to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "text-field__input"))
)

# Step 1: Enter your email address and submit
if send_keys_safe(driver, By.CLASS_NAME, "text-field__input", "reddy_bhavya@icloud.com", wait_time=10, retries=5):
    print("Email entered successfully.")
else:
    print("Failed to enter email.")

# Wait a moment for the page to update (the input field should now be for the password)
time.sleep(2)

# Step 2: Enter your password and submit
if send_keys_safe(driver, By.CLASS_NAME, "text-field__input", "VF4J8tiHx3Ldc", wait_time=10, retries=5):
    print("Password entered successfully.")
else:
    print("Failed to enter password.")

# Allow time for the login process to complete and session cookies to be set
time.sleep(5)

# -------------------------------
# Navigate to the target page
# -------------------------------

target_url = "https://www.vogue.com/slideshow/2025-awards-season-dream-dress-runway"
driver.get(target_url)

# Wait for the page to load; here we wait until the body is present
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)

print("Navigated to the slideshow page.")

# -------------------------------
# Scroll to load more captions
# -------------------------------

# Initial scroll position
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    
    # Scroll down by 1/3 of the page height
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight/3);")
    
    # Wait a moment for the page to load more content
    time.sleep(3)
    
    # Calculate the new scroll height and compare it with the last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # If the scroll height hasn't changed, we have reached the end of the page
    if new_height == last_height:
        break
    
    last_height = new_height  # Update the last height

# Optionally, wait a little longer after the final scroll
time.sleep(3)

# -------------------------------
# Extract content using BeautifulSoup
# -------------------------------

# Get the page source and parse it with BeautifulSoup
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

# Extract the main article text from the container div that holds your paragraphs.
article_text = ""
for p in soup.find_all("p"):
    article_text += p.get_text(separator=" ", strip=True) + "\n\n"

# Find all span elements with the given class (captions).
caption_elements = soup.find_all("span", class_="GallerySlideCaptionHedText-iqjOmM jwPuvZ")
# Extract the text from each caption element and join them with newlines.
captions_text = "\n".join(caption.get_text(strip=True) for caption in caption_elements)

# Combine the article text and caption
full_text = "Article Text:\n" + article_text + "\n\nCaption:\n" + captions_text

# Save the extracted text to a text file
with open("vogue_article.txt", "w", encoding="utf-8") as file:
    file.write(full_text)

print("Extracted content saved to vogue_article.txt.")

# -------------------------------
# Cleanup
# -------------------------------
time.sleep(5)
driver.quit()