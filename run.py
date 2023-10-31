import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.parse import urlparse
from loguru import logger
from websites import websites


MAX_DEPTH = 2

# keep dictionary of website urls with text as value
url_text_dict: dict[str, str] = {}


# return list of found URLs on the website
def extract_text_from_url(url: str, current_depth: int):
    logger.debug(f"Extrahiere: {url=} {current_depth=}")

    # check if this page was already downloaded/checked for links
    if url in url_text_dict.keys():
        logger.debug(f"Url {url} bereits ueberprueft")
        return
    else:
        driver.get(url)

        # time.sleep(2)
        # if not, save text in dictionary
        url_text_dict[url] = driver.find_element(By.TAG_NAME, "body").text

        link_elements = driver.find_elements(By.TAG_NAME, "a")
        urls = [link.get_attribute("href") for link in link_elements]  # type: ignore
        urls = [url for url in urls if url is not None]
        filtered_urls = [s for s in urls if s.startswith(url)]

        if current_depth < MAX_DEPTH:
            for url in filtered_urls:
                extract_text_from_url(url, current_depth + 1)
        else:
            logger.info("MAX_DEPTH erreicht, keine weitere Ueberpruefung von Urls")


if __name__ == "__main__":
    logger.info("Setup Browser...")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # type: ignore
    driver = webdriver.Chrome(options=options)

    logger.info("Starte Textextraktion...")
    for website_url in websites:
        logger.info(f"Haupt URL: {website_url}")
        # empty dictionary
        url_text_dict = {}
        url_text_dict_unique: dict[str, str] = {}
        extract_text_from_url(website_url, 0)

        # remove duplicate values
        # Iterate through the original dictionary
        for url, text in url_text_dict.items():
            # Check if the value is not already in the unique_dict
            if text not in url_text_dict_unique.values():
                # Add the key-value pair to the unique_dict
                url_text_dict_unique[url] = text

        logger.info("Speichere Textdateien...")

        for url, text in url_text_dict_unique.items():
            foldername = os.path.join(
                "website-texts", website_url.replace("https://", "")
            )
            os.makedirs(foldername, exist_ok=True)

            filename = url.replace("https://", "")
            filename = filename.replace("https://", "")
            filename = filename.replace("/", "__")
            filename = filename.replace("?", "___")

            logger.debug(f"Speichere {filename}")
            with open(
                os.path.join(foldername, f"{filename}.txt"),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(text)

    driver.quit()
