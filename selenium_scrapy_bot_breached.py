import pytomlpp
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

CREDENTIALS = './credentials.toml'

def load_credentials(path: str) -> tuple:
    with open(path, 'r') as toml_file:
        contents = pytomlpp.load(toml_file)

    username = contents["breachedto"]["username"]
    password = contents["breachedto"]["password"]
    # my_post_key = get_my_post_key()
    my_post_key = get_my_post_key()

    return username, password, my_post_key

def get_my_post_key() -> str:
    return browser.find_element(By.XPATH, '/html/body/div[1]/main/form/input[3]').get_attribute('value')

def open_browser() -> WebDriver:
    return webdriver.Chrome()

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

def check_login_sucessful():
    print('Login successful') if browser.find_element(By.CLASS_NAME, 'rf_noob') else print('Something went wrong on login')

def go_to_page(url) -> None:
    browser.get(url)

def make_search():
    keyword = 'vulnerability'
    # keywords = ['vulnerability', 'exploit']
    search_field = browser.find_element(By.NAME, 'keywords')
    search_button = browser.find_element(By.NAME, 'submit')

    search_field.send_keys(keyword)
    search_button.click()

def enter_thread():
    raise NotImplementedError

def extract_contents():
    raise NotImplementedError

def next_page_present():
    raise NotImplementedError

browser = open_browser()
go_to_page('https://breached.to/member?action=login')
username, password, my_post_key = load_credentials(CREDENTIALS)
html_content = selenium_page_source(browser)
scrapy_selector = Selector(text=html_content)
# selenium_html_response = browser.page_source
print(scrapy_selector.xpath('/html/head/title/text()').get())

xpath_login = '/html/body/div[1]/header/nav/div/ul/li[1]/a/@href'
xpath_register = '/html/body/div[1]/header/nav/div/ul/li[2]/a/@href'

print(scrapy_selector.xpath(xpath_login).get())
print(scrapy_selector.xpath(xpath_register).get())

goto_login_page(username, password, my_post_key)
print(scrapy_selector.xpath('/html/head/title/text()').get())

go_to_page('https://breached.to/search')
make_search()

close_browser()
