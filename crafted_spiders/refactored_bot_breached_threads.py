#!/home/user/Documents/COGNOS/venv_cognos/bin/python3.10
import time
import logging

import pytomlpp
import tbselenium.common as cm

# from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

# For problems when some object is not loaded
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_bot_breached_dataclass import Selenium_Cognos_Dataclass_Breached

# from stem.util import term
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import launch_tbb_tor_with_stem

CREDENTIALS_PATH = "/home/user/Documents/COGNOS/crafted_spiders/cred.toml"
SCRAPED_PATHS_VULN = "../../results/scraped_paths_vulnerability.txt"
SCRAPED_PATHS_XPL = "../../results/scraped_paths_exploit.txt"

urls = {
    "breached_hidden_service_base": "http://breached65xqh64s7xbkvqgg7bmj4nj7656hcb7x4g42x753r7zmejqd.onion",
    "breached_login_hidden_service": "http://breached65xqh64s7xbkvqgg7bmj4nj7656hcb7x4g42x753r7zmejqd.onion/login",
    "check_tor": "https://check.torproject.org/",
}


class BreachedSpider_Threads:
    def __init__(
        self,
        filename: str,
        filepath: str,
        file_extension: str = ".txt",
        tbb_dir: str = "/home/user/Documents/COGNOS/crafted_spiders/tor-browser_en-US",
    ) -> None:
        self.tbb_dir = tbb_dir
        self.filename = filename
        self.filepath = filepath
        self.file_extension = file_extension
        self.logger = self.setup_logging()

    def setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("selenium_log_threads")
        logger.setLevel(logging.DEBUG)
        selenium_logger_handler = logging.FileHandler("selenium_log_threads.log")
        selenium_formatter = logging.Formatter("[%(asctime)s] %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s")
        selenium_logger_handler.setFormatter(selenium_formatter)
        logger.addHandler(selenium_logger_handler)

        return logger

    def setup_browser(self) -> WebDriver:
        try:
            self.logger.debug("Opening tor browser...")
            tor_process = launch_tbb_tor_with_stem(tbb_path=self.tbb_dir)
            self.logger.debug(f"Tor process: {tor_process}")
            browser = TorBrowserDriver(self.tbb_dir, tor_cfg=cm.USE_STEM)

            return browser
        except OSError as e:
            self.logger.debug(f"Something went wrong: {e}")

    def load_credentials(self, filename: str) -> tuple:
        with open(filename, "r") as toml_file:
            contents = pytomlpp.load(toml_file)

        username = contents["breachedto"]["username"]
        password = contents["breachedto"]["password"]

        return username, password

    def login(self, username: str, password: str, browser: WebDriver) -> None:
        # 1 go to login page
        # 2 login
        username_field = browser.find_element(By.NAME, "username")
        password_field = browser.find_element(By.NAME, "password")
        login_button = browser.find_element(By.NAME, "submit")
        username_field.send_keys(username)
        password_field.send_keys(password)
        time.sleep(30)
        login_button.click()
        # 3 check_login_succesul
        if self.check_login_succesful(browser) == False:
            self.logger.debug("Oops, something went wrong")
            self.close_browser()

    def check_login_succesful(self, browser: WebDriver) -> bool:
        try:
            badge = WebDriverWait(browser, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "rf_noob"))
            )
            if badge:
                self.logger.debug("Login successul")
                return True
            # if browser.find_element(By.CLASS_NAME, "rf_noob"):
        except NoSuchElementException as e:
            self.logger.debug("Exception ocurred!")
            self.logger.debug(f"Message: {e.msg}")
            self.logger.debug(f"Stacktrace: {e.stacktrace}")
            return False

    def go_to_page(self, browser: WebDriver, url: str) -> None:
        browser.load_url(url, wait_for_page_body=True)

    @classmethod
    def write_to_file(
        cls, item: list, filename: str, filepath: str, file_extension: str = ".txt"
    ) -> None:
        with open(
            f"{filepath}{filename}{file_extension}", mode="a+"
        ) as scraped_results:
            if scraped_results.writable():
                for i in item:
                    scraped_results.write(i)

    def go_to_next_page(self, browser: WebDriver) -> None:
        xpath_next_page_pattern = '/html//a[@class = "pagination_next"]'
        next_page_button_present = WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.XPATH, xpath_next_page_pattern))
        )

        if next_page_button_present:
            next_page_button = browser.find_element(By.XPATH, xpath_next_page_pattern)
            next_page_button.click()

    def next_page_present(self, browser: WebDriver) -> bool:
        xpath_next_page_pattern = '/html//a[@class = "pagination_next"]'
        try:
            next_page_button_present = WebDriverWait(browser, 60).until(
                EC.presence_of_element_located((By.XPATH, xpath_next_page_pattern))
            )
        except NoSuchElementException:
            return False

        if next_page_button_present is not None:
            return True

    @staticmethod
    def load_paths(filepath: str) -> list:
        with open(filepath, "r") as file:
            paths = file.readlines()

        return paths

    def extract_contents_from_post(self, browser: WebDriver) -> None:
        self.logger.debug(f"Received argument browser {browser}")

        xpath_title = "/html/body/div[1]/main/table[1]/tbody/tr[1]/td/div/span"
        title = WebDriverWait(browser, 120).until(
            EC.presence_of_element_located((By.XPATH, xpath_title))
        )
        self.logger.debug(f"Title from browser: {title}")

        xpath_posts = '//*[@id="posts"]'
        xpath_post_contents = '//*[@id="posts"]/div[*]/div[2]/div[1]/div[2]'

        next_page_exists = self.next_page_present(browser)

        while next_page_exists != False:
            time.sleep(10)

            posts = browser.find_elements(By.XPATH, xpath_posts)
            self.logger.debug(f"Posts type: {type(posts)}")
            self.logger.debug(f"{posts}")

            for _ in posts:
                post_contents = WebDriverWait(browser, 120).until(
                    EC.any_of(
                        EC.visibility_of_all_elements_located((By.XPATH, xpath_post_contents)),
                        EC.presence_of_all_elements_located((By.CLASS_NAME, '.post_body'))
                    )
                )

            post_content = [f'{content.text}\n' for content in post_contents]
            self.logger.debug(f"{post_content}")

            BreachedSpider_Threads.write_to_file(
                post_content, filename="scraped_posts_vulnerability_dev", filepath="../../results/"
            )

            next_page_exists = self.next_page_present(browser)

            if next_page_exists:
                self.go_to_next_page(browser)

    def scrape_threads(self):
        self.logger.debug("Logger created.")
        try:
            self.logger.debug("Opening browser...")
            browser = self.setup_browser()
            self.logger.debug("Browser opened.")

            self.logger.debug("Going to the login page...")
            self.go_to_page(
                browser,
                urls.get(
                    "breached_login_hidden_service", "URL not registered in the dict"
                ),
            )

            self.logger.debug("Loading credentials...")
            username, password = self.load_credentials(CREDENTIALS_PATH)
            self.logger.debug("Logging in...")
            self.login(username, password, browser)

            self.logger.debug(f"{SCRAPED_PATHS_VULN}")
            paths_to_scrape = BreachedSpider_Threads.load_paths(SCRAPED_PATHS_VULN)
            self.logger.debug(f"Paths to scrape [:10]: {paths_to_scrape[:10]}")

            for path in paths_to_scrape:
                self.logger.debug(f"Entering the path: {path}")
                self.go_to_page(browser, path)
                self.extract_contents_from_post(browser)

        except NoSuchElementException as e:
            self.logger.debug("Something went wrong.")
            self.logger.debug(f"Exception: {e.msg}")
            self.logger.debug(f"Stacktrace: {e.stacktrace}")


spider = BreachedSpider_Threads("scraped_posts", "../../")
spider.scrape_threads()
