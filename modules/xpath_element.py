from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as es
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By


def exception_element(driver, path):
    try:
        wait = WebDriverWait(driver, 5)
        element = wait.until(es.presence_of_element_located((By.XPATH, path)))
        return element

    except TimeoutException:
        return
