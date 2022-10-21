import uuid
import logging
import pytomlpp
import tbselenium.common as cm
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import launch_tbb_tor_with_stem
from scrapy import Selector
# from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_scrapy_bot_breached_dataclass import Selenium_Scrapy_Cognos_Dataclass_Breached

CREDENTIALS = 'spiders/cognos/spiders_credentials/credentials.toml'
logging.basicConfig(level=logging.DEBUG)

def load_credentials(path: str) -> tuple:
    with open(path, 'r') as toml_file:
        contents = pytomlpp.load(toml_file)

    username = contents["breachedto"]["username"]
    password = contents["breachedto"]["password"]
    my_post_key = get_my_post_key()

    return username, password, my_post_key

def get_my_post_key() -> str:
    return browser.find_element(By.XPATH, '/html/body/div[1]/main/form/input[3]').get_attribute('value')

def open_browser() -> WebDriver:
<<<<<<< HEAD

    return webdriver.Chrome()

=======
	browser = TorBrowserDriver(tbb_dir, tor_cfg=cm.USE_STEM)
	return browser
    
>>>>>>> d823868 (Commitando arquivos para automatizar o TorBrowser)
def close_browser() -> None:
    browser.close()

def login(username: str, password: str, post_key: str) -> None:
    username_field = browser.find_element(By.NAME, 'username')
    password_field = browser.find_element(By.NAME, 'password')
    login_button = browser.find_element(By.NAME, 'submit')
    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

def selenium_page_source(browser: WebDriver) -> str:
    return browser.page_source

def goto_login_page(username: str, password: str, post_key: str) -> None:
    # Find the login page and navigate to the page
    login_element = browser.find_element(By.CLASS_NAME, 'panel__module')
    login_element.click()
    assert 'BreachForums - Login' in browser.title
    login(username, password, post_key)
    check_login_sucessful()

def check_login_sucessful() -> None:
    print('Login successful') if browser.find_element(By.CLASS_NAME, 'rf_noob') else print('Something went wrong on login')

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

def get_path_all_threads(html_content: Selector) -> list:
    css_thread_post_pattern = 'tr.inline_row:nth-child(n) > td:nth-child(n) > div:nth-child(n) > span:nth-child(n) > a:nth-child(n)::attr(href)'
    paths = html_content.css(css_thread_post_pattern).getall()

    for path in paths:
        go_to_page(f'https://breached.to/{path}')
        html_content = selenium_page_source(browser)
        extract_contents_from_posts(Selector(text=html_content))

def extract_contents_from_posts(html_content: Selector) -> str:
    item = Selenium_Scrapy_Cognos_Dataclass_Breached()
    item.uuid(uuid.uuid4())
    item.title('title path here')
    item.username('username path here')
    item.info_date_post('info_date_post path here')
    item.post_content('post_content path here')
    item.url('url path here')
    logging.info(html_content.xpath('/html/head/title/text()').get())
    save_to_json(item)

    if next_page_present():
        click_next_page()
        extract_contents_from_posts(html_content)

def save_to_json():
    raise NotImplementedError

def click_next_page() -> None:
    next_page_button = browser.find_element(By.CLASS_NAME, 'pagination_next')
    next_page_button.click()

def next_page_present() -> bool:
    xpath_next_page_pattern = '/html//a[@class = "pagination_next"]/@href'
    xpath_next_page = Selector.xpath(xpath_next_page_pattern).get()

    if xpath_next_page is not None:
        return True

    return False

<<<<<<< HEAD
if __name__ == '__main__':
    browser = open_browser()
    go_to_page('https://breached.to')
    go_to_page('https://breached.to/member?action=login')
    username, password, my_post_key = load_credentials(CREDENTIALS)
    html_content = selenium_page_source(browser)
    scrapy_selector = Selector(text=html_content)
    # selenium_html_response = browser.page_source
    logging.info(scrapy_selector.xpath('/html/head/title/text()').get())
    xpath_login = '/html/body/div[1]/header/nav/div/ul/li[1]/a/@href'
    xpath_register = '/html/body/div[1]/header/nav/div/ul/li[2]/a/@href'
=======
urls = {
	'breached_login_hidden_service': 'http://breached65xqh64s7xbkvqgg7bmj4nj7656hcb7x4g42x753r7zmejqd.onion/login',
	'check_tor': 'https://check.torproject.org/'
}

tbb_dir = "/home/user/Documents/COGNOS/crafted_spiders/tor-browser_en-US"
tor_process = launch_tbb_tor_with_stem(tbb_path=tbb_dir)

browser = open_browser()
go_to_page(urls.get('breached_login_hidden_service', 'URL not registered'))
# go_to_page(check_tor)
username, password, my_post_key = load_credentials(CREDENTIALS)
html_content = selenium_page_source(browser)
scrapy_selector = Selector(text=html_content)
# selenium_html_response = browser.page_source
logging.info(scrapy_selector.xpath('/html/head/title/text()').get())
>>>>>>> d823868 (Commitando arquivos para automatizar o TorBrowser)

    logging.info(scrapy_selector.xpath(xpath_login).get())
    logging.info(scrapy_selector.xpath(xpath_register).get())

    goto_login_page(username, password, my_post_key)
    logging.info(scrapy_selector.xpath('/html/head/title/text()').get())

    go_to_page('https://breached.to/search')
    make_search()
    html_content = selenium_page_source(browser)
    scrapy_selector = Selector(text=html_content)
    get_path_all_threads(scrapy_selector)
    close_browser()
