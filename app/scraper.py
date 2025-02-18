from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self):
        self.driver = None
        self._init_driver()
        logger.info("Scraper initialized with WebDriver")

    def _init_driver(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            # Add performance options
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.page_load_strategy = "eager"  # Don't wait for all resources

            self.driver = webdriver.Remote(
                command_executor="http://selenium-chrome:4444/wd/hub",
                options=chrome_options,
            )
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def get_page_content(self, manga_link: str) -> str:
        try:
            if self.driver is None:
                self._init_driver()

            logger.info(f"Fetching content from: {manga_link}")
            self.driver.get(manga_link)

            try:
                # Check if the page is blocked
                if "请点击此处继续阅读！" not in self.driver.page_source:
                    raise TimeoutException
                logger.info("Content barrier found, attempting to bypass...")

                element = WebDriverWait(self.driver, 5).until(
                    EC.all_of(
                        EC.presence_of_element_located((By.ID, "checkAdult")),
                        EC.element_to_be_clickable((By.ID, "checkAdult")),
                        EC.visibility_of_element_located((By.ID, "checkAdult")),
                    )
                )[0]

                if element.is_displayed() and element.is_enabled():
                    self.driver.execute_script("arguments[0].click();", element)
                else:
                    logger.warning("Content barrier detected but not clickable")
                    return None

            except TimeoutException:
                logger.info("No content barrier found, proceeding...")

            # Wait for essential content only
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "chapter-list"))
            )

            return self.driver.page_source

        except Exception as e:
            logger.error(f"Error fetching page: {str(e)}")
            self.cleanup()  # Reset driver on error
            self.driver = None
            raise

    def cleanup(self):
        try:
            if self.driver:
                self.driver.quit()
                logger.info("Selenium chrome session cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
