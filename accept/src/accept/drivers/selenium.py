from time import sleep

from httpx import Client
from selenium.webdriver.chrome.webdriver import WebDriver

from accept.driver import Driver, Connection
from accept.drivers.http import HttpDriver
from backend.lobby.schemas import LobbyResponse
from bot.browser import connect, start_browser

_WS_INTERCEPTOR = """
(function() {
    const orig = EventTarget.prototype.addEventListener;
    EventTarget.prototype.addEventListener = function(type, listener, ...opts) {
        if (this instanceof WebSocket && type === 'message') {
            const wrapped = function(event) {
                try {
                    const data = JSON.parse(event.data);
                    if (data && data.topcard) window.__gameState = data;
                } catch(e) {}
                return listener.call(this, event);
            };
            return orig.call(this, type, wrapped, ...opts);
        }
        return orig.call(this, type, listener, ...opts);
    };
})();
"""


def _inject_interceptor(browser: WebDriver):
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": _WS_INTERCEPTOR})


class SeleniumDriver(Driver):
    def __init__(self) -> None:
        self.http_driver = HttpDriver(Client(base_url="http://localhost:8000"))
        self.browser1 = connect(5001)
        self.browser2 = start_browser(5002, "user2")
        _inject_interceptor(self.browser1)
        _inject_interceptor(self.browser2)
        self._home_count = 0

    def home(self):
        from accept.screens.selenium import SeleniumBrowserHomeScreen
        index = self._home_count
        self._home_count += 1
        browser = self.browser1 if index == 0 else self.browser2
        return SeleniumBrowserHomeScreen(browser)

    def create_and_join_lobby(self, config: dict) -> LobbyResponse:
        return self.http_driver.create_and_join_lobby(config)

    def get_lobbies(self) -> list[LobbyResponse]:
        return self.http_driver.get_lobbies()

    def join_lobby(self, lobby: LobbyResponse, username: str) -> Connection:
        return self.http_driver.join_lobby(lobby, username)
