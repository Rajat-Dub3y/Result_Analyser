from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import time
import json
import os

BASE_URL = "https://hit.ucanapply.com"

# ---------- Load Creds ----------
with open("creds.json", "r") as f:
    creds = json.load(f)

START_ROLL = creds["START_ROLL"]
END_ROLL = creds["END_ROLL"]
YOUR_ROLL = creds["YOUR_ROLL"]
YOUR_PASSWORD = creds["YOUR_PASSWORD"]

# ---------- Create Downloads Folder ----------
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ---------- Setup Selenium ----------
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# ---------- LOGIN ----------
driver.get(BASE_URL)

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Student Login')]/.."))
).click()

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "loginform")))

driver.find_element(By.ID, "username").send_keys(YOUR_ROLL)
driver.find_element(By.ID, "password").send_keys(YOUR_PASSWORD)
driver.find_element(By.XPATH, "//span[text()='Sign In']").click()

# ---------- GO TO Student Activity ----------
driver.get(BASE_URL + "/student/student-activity")

# ---------- Locate Fifth Semester Form ----------
fifth_form = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((
        By.XPATH,
        "//td[contains(text(),'Fifth Semester')]/../td/form"
    ))
)

# Extract POST target URL + CSRF token
action_url = fifth_form.get_attribute("action")
csrf = fifth_form.find_element(By.NAME, "_token").get_attribute("value")

print("Action URL:", action_url)
print("CSRF token:", csrf)

# ---------- Extract cookies for requests session ----------
cookies = {c['name']: c['value'] for c in driver.get_cookies()}
session = requests.Session()
for k, v in cookies.items():
    session.cookies.set(k, v)

print("\nSession ready. Starting downloads...\n")

# ---------- Loop & Download PDFs ----------
for roll in range(START_ROLL, END_ROLL + 1):
    print(f"Fetching roll: {roll}")

    data = {
        "rollno": str(roll),
        "provisional": "N",
        "_token": csrf
    }

    try:
        r = session.post(action_url, data=data)

        if r.headers.get("Content-Type", "").startswith("application/pdf"):
            file_path = os.path.join(DOWNLOAD_DIR, f"{roll}.pdf")
            with open(file_path, "wb") as f:
                f.write(r.content)
            print(f"✔ Saved {file_path}")
        else:
            print(f"✖ No PDF for roll {roll} (maybe not declared yet)")

    except Exception as e:
        print(f"Error for {roll}: {e}")

    time.sleep(0.3)

driver.quit()
print("\nDONE.\n")
