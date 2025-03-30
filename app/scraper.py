from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import os
import time
from lru_cache_with_ttl import LRUCacheWithExpiration
from rate_limiter import RateLimiter

logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self):
        self.driver = None
        self._init_driver()
        self.cache_ttl = 12 * 3600  # 12 hours in seconds
        self.cache = LRUCacheWithExpiration(maxsize=100, ttl=self.cache_ttl)
        self.rate_limiter = RateLimiter(
            tokens_per_second=0.25, max_tokens=1.0
        )  # 1 request per 4 seconds
        logger.info("Scraper initialized with WebDriver and rate limiter")

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

            selenium_url = os.getenv(
                "SELENIUM_URL", "http://selenium-chrome:4444/wd/hub"
            )
            self.driver = webdriver.Remote(
                command_executor=selenium_url,
                options=chrome_options,
            )
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def _get_page_content_with_timestamp(self, manga_link: str) -> str:
        """Internal method to fetch page content with timestamp"""
        try:
            if self.driver is None:
                self._init_driver()

            # Acquire rate limit token before making request
            self.rate_limiter.acquire()

            logger.info(
                "Fetching manga content from source", extra={"manga_link": manga_link}
            )
            self.driver.get(manga_link)

            try:
                # Check if the page is blocked
                if "请点击此处继续阅读！" not in self.driver.page_source:
                    raise TimeoutException
                logger.debug("Content barrier found, attempting bypass")

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
                    return None, 0

            except TimeoutException:
                logger.debug("No content barrier found")

            # Wait for essential content
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "chapter-list"))
            )

            return self.driver.page_source

        except Exception as e:
            logger.error(
                "Error fetching page",
                extra={
                    "manga_link": manga_link,
                    "error": str(e),
                    "error_type": type(e).__name__,
                },
            )
            self.cleanup()
            self.driver = None
            raise

    def get_page_content(self, manga_link: str, force_refresh: bool = False) -> str:
        """Public method that handles cache invalidation based on TTL"""
        try:
            if not force_refresh and manga_link in self.cache:
                logger.debug(
                    "Using cached content for manga_link",
                    extra={"manga_link": manga_link},
                )
                return self.cache.get(manga_link)[0]  # return the content

            content = self._get_page_content_with_timestamp(manga_link)
            if content is None:
                return None

            self.cache[manga_link] = (content, time.time())
            return content

        except Exception as e:
            logger.error(f"Error in get_page_content: {str(e)}")
            return None

    def cleanup(self):
        try:
            if self.driver:
                self.driver.quit()
                self.cache = None
                logger.info("Selenium chrome session and cache cleaned up")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
