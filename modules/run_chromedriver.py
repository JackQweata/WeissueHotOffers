from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from fake_headers import Headers


def get_chromedriver(use_proxy=False):
    try:
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--user-agent=%s' % Headers(headers=True).generate())
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.headless = True   # фоновый режим
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver
    except WebDriverException:
        return
