from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    NoSuchElementException,
    ElementNotInteractableException,
)
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome()
            logger.info("Chrome WebDriver initialized successfully")
        except WebDriverException as e:
            logger.error(f"Failed to initialize Chrome WebDriver: {str(e)}")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    def get_page_content(self, manga_link: str) -> str:
        try:
            logger.info(f"Attempting to fetch content from: {manga_link}")
            self.driver.get(manga_link)

            # Wait for page load instead of fixed sleep
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            try:
                element = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.ID, "checkAdult"))
                )

                if element.is_displayed() and element.is_enabled():
                    logger.info("Content barrier found, attempting to bypass...")
                    self.driver.execute_script("arguments[0].click();", element)
                elif element.is_displayed() or not element.is_enabled():
                    logger.warning("Content barrier detected but not clickable")
                    return None

            except TimeoutException:
                logger.info("No content barrier found, proceeding...")

            page_source = self.driver.page_source
            logger.info("Successfully retrieved page content")
            return page_source

        except TimeoutException as e:
            logger.error(f"Timeout while loading page: {str(e)}")
            raise
        except WebDriverException as e:
            logger.error(f"WebDriver error: {str(e)}")
            raise

    def cleanup(self):
        try:
            self.driver.quit()
            logger.info("Browser session cleaned up successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
