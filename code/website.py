from dataclasses import dataclass
from typing import Any
from loguru import logger
from configuration import Configuration
from selenium import webdriver
from selenium.webdriver.common.by import By


@dataclass
class WebsiteContent:
    text: str
    subsites: dict[str, "WebsiteContent"]  # key is also url


def extract_all(
    browser: webdriver.Chrome,
    max_depth: int,
    current_depth: int,
    url: str,
    global_url_list: list[str],
) -> WebsiteContent:
    logger.info(f"Analysiere {url} bei Tiefe {current_depth}")
    global_url_list.append(url)

    browser.get(url)

    # fill with text from page
    current_content = WebsiteContent(
        text=browser.find_element(By.TAG_NAME, "body").text, subsites={}
    )

    # now look for links
    link_elements = browser.find_elements(By.TAG_NAME, "a")
    urls = [link.get_attribute("href") for link in link_elements]  # type: ignore
    urls = [url for url in urls if url is not None]

    # only look at urls that point to a deeper level, not so youtube or whatever
    filtered_urls = [s for s in urls if s.startswith(url)]
    # ignore special urls (anchors, search forms)
    filtered_urls = [s for s in filtered_urls if "#" not in s]
    filtered_urls = [s for s in filtered_urls if "?" not in s]
    # sometimes urls end with /, remove for clarity
    filtered_urls = [s.rstrip("/") if s.endswith("/") else s for s in filtered_urls]

    if current_depth < max_depth:
        for url in filtered_urls:
            if url not in global_url_list:
                current_content.subsites[url] = extract_all(
                    browser, max_depth, current_depth + 1, url, global_url_list
                )
            else:
                logger.debug(f"Ignoriere bereits überprüfte url {url}")
    else:
        logger.info("MAX_DEPTH erreicht, keine weitere Ueberpruefung von Urls")

    return current_content


# # return list of found URLs on the website
# def extract_text_from_url(url: str, current_depth: int):
#     logger.debug(f"Extrahiere: {url=} {current_depth=}")

#     # check if this page was already downloaded/checked for links
#     if url in url_text_dict.keys():
#         logger.debug(f"Url {url} bereits ueberprueft")
#         return
#     else:
#         driver.get(url)

#         # time.sleep(2)
#         # if not, save text in dictionary
#         url_text_dict[url] = driver.find_element(By.TAG_NAME, "body").text

#         link_elements = driver.find_elements(By.TAG_NAME, "a")
#         urls = [link.get_attribute("href") for link in link_elements]  # type: ignore
#         urls = [url for url in urls if url is not None]
#         filtered_urls = [s for s in urls if s.startswith(url)]

#         if current_depth < MAX_DEPTH:
#             for url in filtered_urls:
#                 extract_text_from_url(url, current_depth + 1)
#         else:
#             logger.info("MAX_DEPTH erreicht, keine weitere Ueberpruefung von Urls")
