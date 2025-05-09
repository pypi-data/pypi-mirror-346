import logging
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Optional, Literal

from .data import (
    valid_countries_iso,
    valid_start_trending,
    valid_category,
    valid_sort_by,
)


logger = logging.getLogger(__name__)

LogMethod = Literal["logger", "print"]


def log_nothing(*args, **kwargs):
    pass


class Website:
    def __init__(self, url: str, log: Optional[LogMethod] = None):
        self.content_logger = log_nothing

        if log == "logger":
            self.content_logger = logger.info
        else:
            self.content_logger = print
        self.url = url
        self.download_dir = os.path.abspath("downloads")
        os.makedirs(self.download_dir, exist_ok=True)

    def scrape_with_selenium(self):
        self.content_logger("Scraping website with Selenium...")
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": self.download_dir,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )

        self.content_logger("Parsing the Output...")
        driver.get(self.url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        self.content_logger("Finding the 'Export' button...")
        export_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[contains(text(),'Export')]]")
            )
        )
        export_btn.click()
        self.content_logger("Clicked the 'Export' button")

        self.content_logger("Finding the 'Download CSV' button")
        csv_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//li[@aria-label='Download CSV']")
            )
        )

        time.sleep(5)

        for idx, btn in enumerate(csv_buttons):
            try:
                driver.execute_script("arguments[0].click();", btn)
            except Exception as e:
                logger.error(f"Failed to click button #{idx + 1}: {e}")

        time.sleep(5)

        driver.quit()

        csv_path: Optional[str] = None

        for file in os.listdir(self.download_dir):
            if file.endswith(".csv"):
                csv_path = os.path.join(self.download_dir, file)
                self.content_logger(f"CSV file downloaded: {csv_path}")
                break

        if csv_path is None:
            os.remove(csv_path)
            raise FileNotFoundError("CSV file was not downloaded.")

        df = pd.read_csv(csv_path)

        os.remove(csv_path)

        return df


def get_trends(url: str, log: Optional[LogMethod] = None) -> pd.DataFrame:
    return Website(url, log).scrape_with_selenium()


def generate_payload(
    geo: str,
    start_trending: Optional[str] = None,
    category: Optional[str] = None,
    trend_status_active_trends: Optional[bool] = None,
    sort_by: Optional[str] = None,
    base_url: Optional[str] = "https://trends.google.com/trending",
) -> str:
    if not geo or geo not in valid_countries_iso:
        raise ValueError(
            f"Invalid `geo` value: {geo}. `geo` is required and it must be one of {valid_countries_iso}"
        )

    base_url += "?geo=" + geo

    if start_trending:
        if start_trending not in valid_start_trending:
            raise ValueError(
                f"Invalid `start_trending` value: {start_trending}. `start_trending` must be one of {valid_start_trending}"
            )
        else:
            if "h" in start_trending:
                base_url += "&hours=" + start_trending.replace("h", "")
            else:
                base_url += "&hours=" + str(int(start_trending.replace("d", "")) * 24)

    if category:
        valid_category_list = list(valid_category.keys())
        if category not in valid_category_list:
            raise ValueError(
                f"Invalid `category` value: {category}. `category` must be one of {valid_category_list}"
            )
        else:
            base_url += "&category=" + str(valid_category[category])

    if trend_status_active_trends:
        base_url += "&status=active"

    if sort_by:
        if sort_by not in valid_sort_by:
            raise ValueError(
                f"Invalid `sort_by` value: {sort_by}. `sort_by` must be one of {valid_sort_by}"
            )
        else:
            base_url += "&sort=" + valid_sort_by[valid_sort_by.index(sort_by)]

    return base_url
