from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from app.scenarious.user_login import LoginPage
from constans import INSTAGRAM_LOGIN
import pickle


class BrowserConnection:

    def __init__(self, name, password):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.name = name
        self.password = password

    def init_cookies(self):
        cookies = pickle.load(open("./cookies/cookie.pkl", "rb"))
        self.browser.add_cookie(cookies)

    def connect_to_instagram(self):
        self.browser.get(INSTAGRAM_LOGIN)
        return LoginPage(self.browser, self.name, self.password)

    def close_browser(self):
        self.browser.close()