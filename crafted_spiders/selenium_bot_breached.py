#!/home/user/Documents/COGNOS/venv_cognos/bin/python3

import os
import uuid
import time
import json
import signal
import logging
import pytomlpp
import tbselenium.common as cm
from stem.util import term
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import launch_tbb_tor_with_stem
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_bot_breached_dataclass import Selenium_Cognos_Dataclass_Breached


# Config stuff, dont edit. I'll move to some conf files or make a database/API to store those infos
CREDENTIALS = '/home/user/Documents/COGNOS/crafted_spiders/cred.toml'
# logging.basicConfig(filename='stem_log.txt', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logging.basicConfig(filename='scrapy_log.txt', filemode='w', level=logging.DEBUG)

# Logger instance
logger = logging.getLogger('selenium_log')
logger.setLevel(logging.DEBUG)

# Handler
selenium_logger_handler = logging.FileHandler('selenium_log.log')

# Log format
selenium_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
selenium_logger_handler.setFormatter(selenium_formatter)

# Adding the handlers to the logger
logger.addHandler(selenium_logger_handler)

# End config stuff

def load_cookie(cookie_file: str) -> None:
    raise NotImplementedError

# Which type return?
def unipckle_cookie(cookie: str):
    raise NotImplementedError

def load_credentials(filename: str) -> tuple:
    with open(filename, 'r') as toml_file:
        contents = pytomlpp.load(toml_file)

    username = contents['breachedto']['username']
    password = contents['breachedto']['password']

    return username, password

def open_browser() -> WebDriver:
    logger.debug('Opening tor browser...')
    tbb_dir = '/home/user/Documents/COGNOS/crafted_spiders/tor-browser_en-US'
    tor_process = launch_tbb_tor_with_stem(tbb_path=tbb_dir)
    browser = TorBrowserDriver(tbb_dir, tor_cfg=cm.USE_STEM)
    return browser

def close_browser() -> None:
    browser.close()

def login(username: str, password: str) -> None:
    username_field = browser.find_element(By.NAME, 'username')
    password_field = browser.find_element(By.NAME, 'password')
    login_button = browser.find_element(By.NAME, 'submit')
    username_field.send_keys(username)
    password_field.send_keys(password)
    time.sleep(45)
    login_button.click()

def selenium_page_source(browser: WebDriver) -> str:
    return browser.page_source

def goto_login_page(username: str, password: str) -> None:
    # Find the login page and navigate to the page
    login_element = browser.find_element(By.CLASS_NAME, 'panel__module')
    login_element.click()
    assert 'BreachForums - Login' in browser.title
    login(username, password)
    check_login_sucessful()

def check_login_sucessful() -> None:
    try:
        if browser.find_element(By.CLASS_NAME, 'rf_noob'):
            logger.debug('Login successful')
    except NoSuchElementException as e:
        logger.debug('Exception ocurred!')
        logger.debug(f'Message: {e.msg}')
        logger.debug(f'Stacktrace: {e.stacktrace}')
    # print('Login successful') if browser.find_element(By.CLASS_NAME, 'rf_noob') else print('Something went wrong on login')

def go_to_page(url: str) -> None:
    # Just a wrapper to get from selenium
    browser.load_url(url, wait_for_page_body=True)

def make_search() -> None:
    keyword = 'vulnerability'
    # keywords = ['vulnerability', 'exploit']
    search_field = browser.find_element(By.NAME, 'keywords')
    search_button = browser.find_element(By.NAME, 'submit')

    search_field.send_keys(keyword)
    search_button.click()

def get_path_all_threads(html_content) -> list:
    css_thread_post_pattern = 'tr.inline_row:nth-child(n) > td:nth-child(n) > div:nth-child(n) > span:nth-child(n) > a:nth-child(even)'
    css_elements = browser.find_elements(By.CSS_SELECTOR, css_thread_post_pattern)
    paths = [elem.get_attribute('href') for elem in css_elements]
    # logger.debug(f'Paths position 1: {paths[0]}')
    # logger.debug(f'Paths position 3: {paths[2]}')
    # logger.debug(f'Paths position 5: {paths[4]}')
    # paths = html_content.css(css_thread_post_pattern).getall()
    # xpath_thread_post_pattern = '/html/body/div/main/table[2]/tbody/tr[*]/td[*]/div/span/a/@href'
    # paths = html_content.xpath(xpath_thread_post_pattern).getall()
    
    for path in paths:
        go_to_page(path)
        # go_to_page(str(urls.get('breached_hidden_service_base', 'URL not registered') + f'/{path}'))
        html_content = selenium_page_source(browser)
        # logger.debug(f'HTML content so far: {html_content}')
        extract_contents_from_posts(html_content)

def extract_contents_from_posts(html_content: str) -> str:
    logger.debug(f'Type of html_content: {type(html_content)}')

    xpath_title = browser.find_element(
        By.XPATH,
        '/html/body/div[1]/main/table[1]/tbody/tr[1]/td/div/span'
    )
    logger.debug(f'Title from browser: {xpath_title.text}')

    logger.debug(f'Content received from get_path_all_threads: {html_content[0:100]}')

    logger.debug('Instantiating dataclass...')
    item = Selenium_Cognos_Dataclass_Breached()

    item.title = browser.find_element(
        By.XPATH,
        '/html/body/div[1]/main/table[1]/tbody/tr[1]/td/div/span'
    ).text
    logger.debug(item.title)

    posts = browser.find_elements(
        By.XPATH,
        '//*[@id="posts"]'
    )

    for post in posts:
        try:
            item.username = post.find_element(
            By.XPATH,
            '/div[*]/div[1]/div[1]/div[1]/div/a/span'
            ).text
            logger.debug(item.username)

            item.info_date_post = post.find_element(
            By.XPATH,
            '/div[*]/div[2]/div[1]/div[1]/span'
            ).text
            logger.debug(item.info_date_post)

            item.post_content = post.find_element(
            By.XPATH,
            '/div[*]/div[2]/div[1]/div[2]'
            ).text
            logger.debug(item.post_content)
        
            item.url = browser.current_url
            logger.debug(item.url)

        except NoSuchElementException as e:
            logger.debug('Exception ocurred!')
            logger.debug(f'Message: {e.msg}')
            logger.debug(f'Stacktrace: {e.stacktrace}')

    logger.debug(f'{item.__dict__}')

    save_to_json(
        file_name='scrape_result',
        file_extension='.json',
        item=item.__dict__,
        file_path='../../'
    )

    if next_page_present():
        click_next_page()
        extract_contents_from_posts(html_content)

def save_to_json(
    file_name: str,
    file_extension: str,
    item: dict[str, any],
    file_path: str = None
    ) -> None:

    logger.debug('Creating the json of results...')
    if file_path is None:
        outfile = open(
            f'{file_name}{file_extension}',
            mode='a+',
            encoding ='utf8'
        )
    else:
        outfile = open(
            f'{file_path}/{file_name}{file_extension}',
            mode='a+',
            encoding ='utf8'
        )
    logger.debug(f'Created json of results: {outfile.name}')
    logger.debug(f'Path of the json: {os.path.realpath(outfile.name)}')

    try:
        json.dump(item, outfile, indent=4)
        # json.dump(item.as_dict(), outfile, indent=4)
    except:
        logger.debug('Something went wrong')
    finally:
        outfile.close()

def click_next_page() -> None:
    next_page_button = browser.find_element(
        By.CLASS_NAME,
        'pagination_next'
    )
    next_page_button.click()

def next_page_present() -> bool:
    xpath_next_page_pattern = '/html//a[@class = "pagination_next"]'
    try:
        next_page_button_present = browser.find_element(
            By.XPATH,
            xpath_next_page_pattern
        )
    except NoSuchElementException as e:
        logger.debug('Exception ocurred!')
        logger.debug(f'Message: {e.msg}')
        logger.debug(f'Stacktrace: {e.stacktrace}')

    if next_page_button_present is not None:
        return True

    return False

urls = {
    'breached_hidden_service_base': 'http://breached65xqh64s7xbkvqgg7bmj4nj7656hcb7x4g42x753r7zmejqd.onion',
    'breached_login_hidden_service': 'http://breached65xqh64s7xbkvqgg7bmj4nj7656hcb7x4g42x753r7zmejqd.onion/login',
    'check_tor': 'https://check.torproject.org/'
}

while True:
    try:
        logger.debug('Starting...')

        browser = open_browser()
        username, password = load_credentials(CREDENTIALS)
        go_to_page(urls.get('breached_login_hidden_service', 'URL not registered'))
        # go_to_page(check_tor)

        html_content = selenium_page_source(browser)
        # selenium_html_response = browser.page_source

        xpath_login = '/html/body/div[1]/header/nav/div/ul/li[1]/a/@href'
        xpath_register = '/html/body/div[1]/header/nav/div/ul/li[2]/a/@href'
        goto_login_page(username, password)
        go_to_page(urls.get('breached_hidden_service_base', 'URL not registered') + '/search')
        make_search()
        html_content = selenium_page_source(browser)
        get_path_all_threads(html_content)
        close_browser()

    except KeyboardInterrupt:
        close_browser()
