from selenium import webdriver
from datetime import datetime
from loguru import logger
import yaml
from code.browser import get_browser
from code.website import extract_all, save_html
from code.configuration import Configuration
import sys


def die():
    logger.info("Zum Verlassen Enter Taste drücken...")
    input()
    sys.exit()


if __name__ == "__main__":
    try:
        logger.info("Öffne Konfiguration...")
        with open("konfiguration.yaml", "r") as file:
            config_dict = yaml.safe_load(file)
            config = Configuration.from_dict(config_dict)
    except (yaml.YAMLError, FileNotFoundError):
        config = Configuration.random_cfg()
        with open("konfiguration.yaml", "w") as file:
            yaml.dump(config.to_dict(), file, default_flow_style=False)
        logger.warning("konfiguration.yaml neu erstellt.")
        logger.warning("konfiguration.yaml anpassen und Programm neu starten!")
        die()

    logger.info("Starte Textextraktion...")
    browser = get_browser()

    for website_url in config.urls:
        logger.info(f"Haupt URL: {website_url}")
        root_website_content = extract_all(
            browser, config.maximum_depth, 0, website_url, []
        )

        filename = (
            website_url.replace("https://", "")
            .replace("https://", "")
            .replace("/", "__")
        )

        save_html(root_website_content, f"{filename}.html")

    die()

    #     # keep dictionary of website urls with text as value
    #     url_text_dict = {}
    #     url_text_dict_unique: dict[str, str] = {}
    #     extract_text_from_url(website_url, 0)

    #     # remove duplicate values
    #     # Iterate through the original dictionary
    #     for url, text in url_text_dict.items():
    #         # Check if the value is not already in the unique_dict
    #         if text not in url_text_dict_unique.values():
    #             # Add the key-value pair to the unique_dict
    #             url_text_dict_unique[url] = text

    #     logger.info("Speichere Textdateien...")

    #     current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    #     logger.debug(f"{current_time=}")

    #     for url, text in url_text_dict_unique.items():
    #         foldername = os.path.join(
    #             "website-texts", website_url.replace("https://", ""), current_time
    #         )
    #         os.makedirs(foldername, exist_ok=True)

    #         filename = url.replace("https://", "")
    #         filename = filename.replace("https://", "")
    #         filename = filename.replace("/", "__")
    #         filename = filename.replace("?", "___")

    #         logger.debug(f"Speichere {filename}")
    #         with open(
    #             os.path.join(foldername, f"{filename}.txt"),
    #             "w",
    #             encoding="utf-8",
    #         ) as f:
    #             f.write(text)

    # driver.quit()
