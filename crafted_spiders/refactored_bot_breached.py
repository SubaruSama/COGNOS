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
        self.logger = self.get_logger()

    def setup_logging(self) -> None:
        logger = logging.getLogger("selenium_log")
        logger.setLevel(logging.DEBUG)
        selenium_logger_handler = logging.FileHandler("selenium_log.log")
        selenium_formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
        selenium_logger_handler.setFormatter(selenium_formatter)
        logger.addHandler(selenium_logger_handler)

    def get_logger(self):
        return self.setup_logging().logger

    def setup_browser(self) -> WebDriver:
        try:
            self.logger.debug("Opening tor browser...")
            tor_process = launch_tbb_tor_with_stem(tbb_path=self.tbb_dir)
            browser = TorBrowserDriver(self.tbb_dir, tor_cfg=cm.USEM_STEM)

            return browser
        except OSError as e:
            self.logger.debug(f"Something went wrong: {e}")

    def get_browser(self) -> WebDriver:
        # 1 setup_browser
        # self.setup_browser()
        # 2 self
        return self.setup_browser().browser

    def close_browser(self) -> None:
        self.browser.quit()

    def load_credentials(self, filename: str) -> tuple:
        with open(filename, "r") as toml_file:
            contents = pytomlpp.load(toml_file)

        username = contents["breachedto"]["username"]
        password = contents["breachedto"]["password"]

        return username, password

    def login(self, username: str, password: str) -> None:
        # 1 load_credentials
        # 2 login
        # 3 check_login_succesul
        pass

    def check_login_succesful(self) -> None:
        pass

    def load_cookise(cookie_file: str) -> None:
        pass

    def unpickle_cookie(cookie: str):
        pass

    @classmethod
    def get_page_source(cls, browser: WebDriver) -> str:
        return browser.page_source

    def go_to_page(self, browser: WebDriver, url: str) -> None:
        browser.load_url(url, wait_for_page_body=True)

    def make_search(self) -> None:
        pass

    def get_path_all_threads(self, html_content: str) -> list:
        # Get the path of ALL threads from ALL results in the results page
        pass

    def extract_contents_from_posts(self, html_content: str) -> str:
        pass

    def enter_thread(self, url: str) -> None:
        self.go_to_page(url)
        pass

    def next_page_present(self) -> bool:
        pass

    def go_to_next_page(self) -> None:
        pass

    @classmethod
    def write_to_file(cls, filename, filepath, file_extension) -> None:
        pass

    def scrape(self):
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
        logger = self.get_logger()
        logger.debug("Logger created.")

        logger.debug("Opening browser...")
        browser = self.get_browser()
        logger.debug("Brownser opened.")

        self.go_to_page("login page")
        self.login()
        self.make_search()

        # Collect all the paths from all threads
        paths = self.get_path_all_threads()
        all_paths_gathered = False
        while all_paths_gathered is not True:
            for path in paths:
                # 1. Collect the path from each thread
                # 2. Check if next page exists
                next_page_present = self.next_page_present()
                if next_page_present:
                    self.go_to_next_page()
                #   2.1 If yes, go to the next page
                #   2.2 If no, start scraping the threads
                pass
            else:
                # Scrape the posts, call the method for it
                all_paths_gathered = True

        # With the list of all threads, enter each thread and collect
        # the posts
        is_scraping_done = False
        urls_from_threads = paths
        while is_scraping_done is not True:
            for url in urls_from_threads:
                self.enter_thread(url)
                post_contents = self.extract_contents_from_posts(html_content)
                BreachedSpider.write_to_file(post_contents)
                next_page_exists = self.next_page_present()
                if next_page_exists:
                    self.go_to_next_page()
                    continue
            else:
                is_scraping_done = True

        self.close_browser()


spider = BreachedSpider("scraped_results", "../../")
spider.scrape()