from selenium import webdriver

class Bot(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def login_admin(self):
        ...

