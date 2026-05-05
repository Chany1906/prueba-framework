from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def test_google_title():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.google.com")
    assert "Google" in driver.title

    driver.quit()