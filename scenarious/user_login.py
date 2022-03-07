from selenium.webdriver.common.by import By
from constans import USERNAME, PASSWORD, SMALL_PAUSE, USERNAME_XPATH, PASSWORD_XPATH, LOGIN_BUTTON
from scenarious.get_profile_info import GetUserInfo


class LoginPage:

    def __init__(self, browser):
        self.browser = browser
        self.username = USERNAME
        self.password = PASSWORD
        self.small_pause = SMALL_PAUSE

    def input_username(self):
        self.browser.implicitly_wait(self.small_pause)
        username_input = self.browser.find_element(By.XPATH, USERNAME_XPATH)
        username_input.send_keys(self.username)

    def input_password(self):
        self.browser.implicitly_wait(self.small_pause)
        password_input = self.browser.find_element(By.XPATH, PASSWORD_XPATH)
        password_input.send_keys(self.password)

    def log_in(self):
        login_button = self.browser.find_element(By.XPATH, LOGIN_BUTTON)
        login_button.click()
        return GetUserInfo(self.browser)