from selenium import webdriver
from selenium.webdriver.firefox.options import *


def create_driver():
    """
        create a selenium web driver using firefox engine
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Firefox(options=options)
    return driver
