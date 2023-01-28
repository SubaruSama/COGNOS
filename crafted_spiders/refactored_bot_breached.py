#!/home/user/Documents/COGNOS/venv_cognos/bin/python3.10

import json
import logging
import os
import sys
import time

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
PATHS = {
    "scraped_paths_file": "../../scraped_paths.txt"
}

urls = {
    "breached_hidden_service_base": "http://breached65xqh64s7xbkvqgg7bmj4nj7656hcb7x4g42x753r7zmejqd.onion",
    "breached_login_hidden_service": "http://breached65xqh64s7xbkvqgg7bmj4nj7656hcb7x4g42x753r7zmejqd.onion/login",
    "breached_hidden_service_search": "http://breached65xqh64s7xbkvqgg7bmj4nj7656hcb7x4g42x753r7zmejqd.onion/search",
    "check_tor": "https://check.torproject.org/",
}

class BreachedSpider:

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
        logger = logging.getLogger("selenium_log")
        logger.setLevel(logging.DEBUG)
        selenium_logger_handler = logging.FileHandler("selenium_log.log")
        selenium_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        selenium_logger_handler.setFormatter(selenium_formatter)
        logger.addHandler(selenium_logger_handler)

        return logger

    # def get_logger(self):
    #     return self.setup_logging().logger

    def setup_browser(self) -> WebDriver:
        try:
            self.logger.debug("Opening tor browser...")
            tor_process = launch_tbb_tor_with_stem(tbb_path=self.tbb_dir)
            browser = TorBrowserDriver(self.tbb_dir, tor_cfg=cm.USE_STEM)

            return browser
        except OSError as e:
            self.logger.debug(f"Something went wrong: {e}")

    # def get_browser(self) -> WebDriver:
    #     # 1 setup_browser
    #     # self.setup_browser()
    #     # 2 self
    #     return self.setup_browser().browser

    def close_browser(self) -> None:
        self.browser.quit()

    def load_credentials(self, filename: str) -> tuple:
        with open(filename, "r") as toml_file:
            contents = pytomlpp.load(toml_file)

        username = contents["breachedto"]["username"]
        password = contents["breachedto"]["password"]

        return username, password

    def login(
        self, username: str, password: str, browser: WebDriver
    ) -> None:
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
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "rf_noob")
                )
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

    def load_cookies(cookie_file: str) -> None:
        pass

    def unpickle_cookie(cookie: str):
        pass

    @classmethod
    def get_page_source(cls, browser: WebDriver) -> str:
        return browser.page_source

    def go_to_page(self, browser: WebDriver, url: str) -> None:
        browser.load_url(url, wait_for_page_body=True)

    def make_search(self, browser: WebDriver) -> None:
        keyword = "vulnerability"
        # keywords = ['vulnerability', 'exploit']
        search_field = browser.find_element(By.NAME, "keywords")
        search_button = browser.find_element(By.NAME, "submit")
        search_field.send_keys(keyword)
        search_button.click()

    def get_path_all_threads(self, browser: WebDriver) -> None:
        # Get the path of ALL threads from ALL results in the results page
        # css_thread_post_pattern = "tr.inline_row:nth-child(n) > td:nth-child(n) > div:nth-child(n) > span:nth-child(n) > a:nth-child(even)"
        # css_thread_post_pattern_tdrow1 = "tr.inline_row > td.trow1:nth-child(3) > div > span > a.subject_new"
        css_thread_post_pattern_tdrow1 = "tr.inline_row > td.trow1:nth-child(3) > div > span > a[class*='subject']"
        # css_thread_post_pattern_tdrow2 = "tr.inline_row > td.trow2:nth-child(3) > div > span > a.subject_new"
        css_thread_post_pattern_tdrow2 = "tr.inline_row > td.trow2:nth-child(3) > div > span > a[class*='subject']"
        tdrow1_present = WebDriverWait(browser, 30).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, css_thread_post_pattern_tdrow1)
                )
            )
        if tdrow1_present:
            css_elements_tdrow1 = browser.find_elements(By.CSS_SELECTOR, css_thread_post_pattern_tdrow1)

        tdrow2_present = WebDriverWait(browser, 30).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, css_thread_post_pattern_tdrow2)
                )
            )
        if tdrow2_present:
            css_elements_tdrow2 = browser.find_elements(By.CSS_SELECTOR, css_thread_post_pattern_tdrow2)

        paths_tdrow1 = [elem.get_attribute("href") for elem in css_elements_tdrow1]
        paths_tdrow2 = [elem.get_attribute("href") for elem in css_elements_tdrow2]

        paths = [*paths_tdrow1, *paths_tdrow2]
        with open(PATHS.get("scraped_paths_file", "File not found"), "a") as file:
            if file.writable():
                for path in paths:
                    file.write(f"{path}\n")

        # Check for next page
        next_page_exists = self.next_page_present(browser)

        if next_page_exists:
            self.go_to_next_page(browser)
            self.get_path_all_threads(browser)
        else:
            return

    def extract_contents_from_posts(self, browser: WebDriver) -> str:
        self.logger.debug(f"Received argument browser {browser}")
        xpath_title = "/html/body/div[1]/main/table[1]/tbody/tr[1]/td/div/span"
        title = browser.find_element(
            By.XPATH, xpath_title
        ).text
        self.logger.debug(f"Title from browser: {title}")

        xpath_posts = '//*[@id="posts"]'
        posts = browser.find_elements(
            By.XPATH, xpath_posts
        )
        self.logger.debug(f"{posts}")

        xpath_post_contents = '/*[@id="posts"]/div[*]/div[2]/div[1]/div[2]'
        for _ in posts:
            post_contents = WebDriverWait(browser, 20).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, xpath_post_contents)
                )
            )

            post_content = [content.text for content in post_contents]
            self.logger.debug(f"{post_content}")

        BreachedSpider.write_to_file(
            post_content,
            filename="scraped_results",
            filepath="../../"
        )

        next_page_exists = self.next_page_present()
        if next_page_exists:
            self.go_to_next_page(browser)
            self.extract_contents_from_posts(browser)

    @staticmethod
    def load_paths(filepath: str) -> list:
        with open(filepath, 'r') as file:
            paths = file.readlines()

        return paths

    def enter_thread(self, url: str) -> None:
        self.go_to_page(url)

    def next_page_present(self, browser: WebDriver) -> bool:
        xpath_next_page_pattern = '/html//a[@class = "pagination_next"]'
        next_page_button_present = WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, xpath_next_page_pattern)
            )
        )

        if next_page_button_present is not None:
            return True
        else:
            return False

    def go_to_next_page(self, browser: WebDriver) -> None:
        next_page_button = browser.find_element(By.CLASS_NAME, "pagination_next")
        next_page_button.click()

    @classmethod
    def write_to_file(cls, item: list, filename: str, filepath: str, file_extension: str = ".txt") -> None:
        with open(f"{filepath}{filename}{file_extension}", mode="a+") as scraped_results:
            if scraped_results.writable():
                for i in item:
                    scraped_results.write(i)

    def scrape(self):
        self.logger.debug("Logger created.")
        # 1. Gerar uma lista com todos os resultados das páginas de buscas,
        #   ir passando para a próxima pagina apenas coletando os paths das threads,
        #   onde irei salvar numa lista e irei passar path a path, sem precisar
        #   me preocupar de voltar pra página e depois checar se tem mais threads
        # 2. Para cada resultado da página de busca:
        #    2.1 Entrar
        #    2.2 Fazer o scrape
        #    2.3 Verificar se tem proxima pagina
        #        2.3.1 Sim: continua
        #        2.3.2 Não: volta para a posição atual + 1 na lista de resultados
        # 3. Checar se a página de busca existe próxima pagina
        #   3.1 Se sim, vai para a proxima pagina e repete o processo
        #   3.2 Se não, termina
        try:
            self.logger.debug("Opening browser...")
            browser = self.setup_browser()
            self.logger.debug("Brownser opened.")

            self.logger.debug(f'Going to the page {urls.get("breached_login_hidden_service", "URL not registered in the dict")}')
            self.go_to_page(browser, urls.get("breached_login_hidden_service", "URL not registered in the dict"))
            self.logger.debug("Loading credentials...")
            username, password = self.load_credentials(CREDENTIALS_PATH)
            self.login(
                username, password, browser
            )

            self.logger.debug(f'Going to the page: {urls.get("breached_hidden_service_search", "URL not registered in the dict")}')
            self.go_to_page(browser, urls.get("breached_hidden_service_search", "URL not registered in the dict"))
            self.make_search(browser)

            # Collect all the paths from all threads
            self.get_path_all_threads(browser)

            self.logger.debug("Loading the paths from file...")
            paths_to_scrape = BreachedSpider.load_paths(PATHS.get("scraped_paths_file", "File not found"))
            self.logger.debug(f"Loaded paths from file: {paths_to_scrape[0:50]}")

            for path in paths_to_scrape:
                self.enter_thread(path)
                self.extract_contents_from_posts(browser)

            self.close_browser()

        except Exception as e:
            self.logger.debug(f"Something went wrong at {self.scrape.__qualname__}!")
            self.logger.debug(f"Exception: {e}")

spider = BreachedSpider("scraped_results", "../../")
spider.scrape()
