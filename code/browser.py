from selenium import webdriver
from loguru import logger


def get_browser() -> webdriver.Chrome:
    logger.info("Setup Browser...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # type: ignore
    return webdriver.Chrome(options=options)
