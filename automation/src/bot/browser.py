from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options


def start_browser(port: int, user: str):
    options = Options()
    options.add_argument(f"--remote-debugging-port={port}")
    options.add_argument(f'user-data-dir=data/{user}')
    driver = WebDriver(options=options) # pyright: ignore[reportCallIssue]
    return driver


def connect(port: int):
    options = Options()
    options.debugger_address = f"127.0.0.1:{port}"
    driver = WebDriver(options)
    driver.implicitly_wait(1)
    return driver