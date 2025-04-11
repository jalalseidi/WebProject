from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
import json

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)


driver.get("http://www.linkedin.com/login")

wait = WebDriverWait(driver, 10)

EMAIL = "matildaseidi@gmail.com"
PASSWORD = "134675Ja"
email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
password_input = driver.find_element(By.ID, "password")

email_input.send_keys(EMAIL)
password_input.send_keys(PASSWORD)

driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()


driver.get("https://www.linkedin.com/jobs/search/?currentJobId=4205414470&f_LF=f_AL&geoId=102257491&keywords=python%20developer&location=London%2C%20England%2C%20United%20Kingdom")


wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.jobs-search__results-list li")))

job_list = []
jobs = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")

for job in jobs:
    try:
        title = job.find_element(By.CSS_SELECTOR, "h3").text
        company = job.find_element(By.CSS_SELECTOR, "h4").text
        link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

        job_list.append({
            "title": title,
            "company": company,
            "link": link
        })
    except Exception as e:
        print("Error scraping job:", e)
        continue

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(job_list, f, ensure_ascii=False, indent=2)

print(f"Saved {len(job_list)} jobs to jobs.json")

