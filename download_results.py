import os
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://hit.ucanapply.com"

with open("creds.json", "r") as f:
    creds = json.load(f)

START_ROLL = creds["START_ROLL"]
END_ROLL = creds["END_ROLL"]
YOUR_ROLL = creds["YOUR_ROLL"]
YOUR_PASSWORD = creds["YOUR_PASSWORD"]

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

SEM_NAMES = [
    "First Semester",
    "Second Semester",
    "Third Semester",
    "Fourth Semester",
    "Fifth Semester"
]

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

print("[*] Logging in...")

driver.get(BASE_URL)

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Student Login')]/.."))
).click()

WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "loginform")))

driver.find_element(By.ID, "username").send_keys(YOUR_ROLL)
driver.find_element(By.ID, "password").send_keys(YOUR_PASSWORD)
driver.find_element(By.XPATH, "//span[text()='Sign In']").click()

print("[*] Opening Student Activity page...")
driver.get(BASE_URL + "/student/student-activity")

# Collect form info for 5 semesters
semester_forms = {}

for i, sem_name in enumerate(SEM_NAMES, start=1):
    form_el = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH,
            f"//td[contains(text(),'{sem_name}')]/../td/form"
        ))
    )
    action_url = form_el.get_attribute("action")
    csrf = form_el.find_element(By.NAME, "_token").get_attribute("value")
    semester_forms[i] = (action_url, csrf)

print("[*] Extracting cookies...")
cookies = {c['name']: c['value'] for c in driver.get_cookies()}

session = requests.Session()
for k, v in cookies.items():
    session.cookies.set(k, v)

print("[*] Starting download of 5 semesters for each roll...\n")

for roll in range(START_ROLL, END_ROLL + 1):
    print(f"[+] Roll: {roll}")

    roll_dir = os.path.join(DOWNLOAD_DIR, str(roll))
    os.makedirs(roll_dir, exist_ok=True)

    for sem in range(1, 6):
        action_url, csrf = semester_forms[sem]

        data = {
            "rollno": str(roll),
            "provisional": "N",
            "_token": csrf
        }

        try:
            r = session.post(action_url, data=data)

            if r.headers.get("Content-Type", "").startswith("application/pdf"):
                file_path = os.path.join(roll_dir, f"sem{sem}.pdf")
                with open(file_path, "wb") as f:
                    f.write(r.content)
                print(f"  ✔ Sem {sem} saved")
            else:
                print(f"  ✖ Sem {sem} not available")

        except Exception as e:
            print(f"  ⚠ Error Sem {sem}: {e}")

        time.sleep(0.2)

print("\n[*] DONE downloading all semesters.")
driver.quit()
