from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from user_login import LoginPage
from constans import INSTAGRAM_LOGIN


class BrowserConnection:

    def __init__(self):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def connect_to_instagram(self):
        self.browser.get(INSTAGRAM_LOGIN)
        return LoginPage(self.browser)

    def close_browser(self):
        self.browser.close()