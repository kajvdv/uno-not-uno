from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver import Keys, ActionChains 


URL = "http://localhost:5173/"

class Bot(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.implicitly_wait(1)


    def login_admin(self):
        self.get(URL)
        username_el = self.find_element(By.ID, 'username')
        username_el.clear()
        username_el.send_keys('admin')

        password_el = self.find_element(By.ID, 'password')
        password_el.clear()
        password_el.send_keys('admin')

        login_but = self.find_element(By.CSS_SELECTOR, '.form-button[value="Login"]')
        login_but.click()
    

    def get_lobbies(self):
        lobbies = []
        self.get(URL + 'lobbies')    
        lobbies = [lobby.text for lobby in self.find_elements(By.CLASS_NAME, 'lobby-join')]

        return lobbies

    def join_lobby(self, lobby_name):
        join_button = self.find_element(By.XPATH, f"//div[contains(@class, 'lobby')][.//h1[text()='{lobby_name}']]//button[contains(text(), 'Join')]")
        join_button.click()

    def play_card(self):
        #TODO Get game from Redis if I've added that
        card_els = [
            elem
            for elem in self.find_elements(By.CSS_SELECTOR, ".hand .card")
        ]
        cards = [
            elem.get_attribute('class')
                .split()[1]
                .split("_")
            for elem in card_els
        ]
        topcard_value, _, topcard_suit = (
            self.find_element(By.CSS_SELECTOR, '.middle .card:last-child')
                .get_attribute('class')
                .split()[1]
                .split("_")
        )
        drawcard_el = self.find_element(By.CSS_SELECTOR, '.middle .card:first-child')
        print("Top card: ", topcard_value, topcard_suit)
        # print(cards)
        for card_el in card_els:
            value, _, suit = card_el.get_attribute('class').split()[1].split("_")
            print(value, suit)
            if value == topcard_value or suit == topcard_suit or topcard_value == 'joker' or value == "joker":
                width = card_el.size['width']
                print(width)
                # return
                off_x = width / -2
                off_y = 0
                ActionChains(self)\
                    .move_to_element_with_offset(card_el, off_x + 1, off_y) \
                    .click() \
                    .perform()
                print(f"playing {value} of {suit}")
                return
        print("Drawing card")
        drawcard_el.click()

    def check_won(self):
        return bool(
            self.find_elements(By.CLASS_NAME, 'game-won-modal')
        )

    def wait_until_turn(self):
        WebDriverWait(self, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.hand.current')))

    def go_back_to_lobbies(self):
        elem = self.find_element(By.CSS_SELECTOR, 'a[href="/lobbies"]')
        elem.click()

