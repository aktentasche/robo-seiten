from dataclasses import dataclass
from loguru import logger
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
    if current_depth < max_depth:
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


def save_html(content: WebsiteContent, filename: str):
    # Generate HTML content recursively for the website structure
    html_content = generate_html(content)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html_content)


def generate_html(content: WebsiteContent) -> str:
    # Recursively generate HTML content for the website structure
    html = f"<div>{content.text}</div>"

    for url, subsite in content.subsites.items():
        # Recursive call to handle subsites
        subsite_html = generate_html(subsite)
        html += f"<h1>Subsite URL: {url}</h1>"
        html += subsite_html

    return html
