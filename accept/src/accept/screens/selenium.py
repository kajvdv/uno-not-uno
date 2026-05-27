from time import sleep
from urllib.parse import urlparse, parse_qs

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumBrowserHomeScreen:
    def __init__(self, browser: WebDriver):
        self._browser = browser

    def create_game(self, size: int, username: str) -> 'SeleniumBrowserLobbyScreen':
        self._browser.get("http://localhost:5173/")
        WebDriverWait(self._browser, 10).until(
            EC.presence_of_element_located((By.ID, "create-new-game"))
        ).click()

        name_input = WebDriverWait(self._browser, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name=name]"))
        )
        name_input.clear()
        name_input.send_keys("test game")

        self._browser.find_element(By.CSS_SELECTOR, ".create-form button[type=submit]").click()

        WebDriverWait(self._browser, 10).until(EC.url_contains("lobby_id"))
        code = parse_qs(urlparse(self._browser.current_url).query)['lobby_id'][0]
        return SeleniumBrowserLobbyScreen(self, self._browser, code, username)

    def join_game(self, code: str, username: str) -> 'SeleniumBrowserLobbyScreen':
        self._browser.get("http://localhost:5173/")
        # Pre-fill the prompt so join() gets the username without user interaction
        self._browser.execute_script(f"window.prompt = () => '{username}';")

        WebDriverWait(self._browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//div[contains(@class,'lobby')][.//h1[text()='{code}']]//button[contains(text(),'Join')]")
            )
        ).click()

        WebDriverWait(self._browser, 10).until(EC.url_contains("lobby_id"))
        return SeleniumBrowserLobbyScreen(self, self._browser, code, username)

    def __eq__(self, other):
        return self is other


class SeleniumBrowserLobbyScreen:
    def __init__(self, home: SeleniumBrowserHomeScreen, browser: WebDriver, code: str, username: str):
        self._home = home
        self._browser = browser
        self._code = code
        self._username = username

    @property
    def code(self) -> str:
        return self._code

    def wait_for_game(self) -> 'SeleniumBrowserGameScreen':
        WebDriverWait(self._browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".player-position-1"))
        )
        return SeleniumBrowserGameScreen(self._home, self._browser, self._username)


class SeleniumBrowserGameScreen:
    def __init__(self, home: SeleniumBrowserHomeScreen, browser: WebDriver, username: str):
        self._home = home
        self._browser = browser
        self._username = username

    @property
    def current_player(self) -> str:
        sleep(0.15)
        state = self._browser.execute_script("return window.__gameState;")
        if state and 'current_player' in state:
            return state['current_player']
        return self._username

    @property
    def winner(self) -> str | None:
        state = self._browser.execute_script("return window.__gameState;")
        if state:
            msg = state.get('message', '')
            if ' has won' in msg:
                return msg.split(' has won')[0]
        return None

    def play_card(self, i: int):
        if i < 0:
            draw_deck = self._browser.find_element(By.CSS_SELECTOR, ".drawdeck")
            self._browser.execute_script("arguments[0].click();", draw_deck)
        else:
            cards = self._browser.find_elements(By.CSS_SELECTOR, ".hand .player .card")
            self._browser.execute_script("arguments[0].click();", cards[i])
        sleep(0.3)

    def exit(self) -> SeleniumBrowserHomeScreen:
        self._browser.find_element(By.CSS_SELECTOR, 'a[href="/lobbies"]').click()
        sleep(0.5)
        return self._home

    def __eq__(self, other):
        return self is other
