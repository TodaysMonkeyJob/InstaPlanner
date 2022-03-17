import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent
from selenium.webdriver.chrome.options import Options

from app.s3_help_functions import read_json_cookies_s3, final_file_cheker
from app.scenarious.get_profile_info import GetUserInfo
from app.scenarious.save_photos import InstaSavePhoto
from constans import *


class IntaLogin:

    def __init__(self, name, password, task):
        self.username = name
        self.password = password
        self.task = task
        self.small_pause = SMALL_PAUSE
        self.medium_pause = MEDIUM_PAUSE

        """Initialize Class."""
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.LINUX.value]

        # Randomized User ID
        user_agent_rotator = UserAgent(software_name=software_names,
                                       operating_systems=operating_systems,
                                       limit=100)
        user_agent = user_agent_rotator.get_random_user_agent()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"user-agent={user_agent}")
        cookies_local_file_path = f'app/tmp/{self.username}_cookies.json'
        cookies_s3_file_path = f'profile/{self.username}/cookies/{self.username}_cookies.json'
        cookie_websites = ['https://Instagram.com']
        self.cookies_s3_file_path = cookies_s3_file_path
        self.cookies_local_file_path = cookies_local_file_path
        self.cookie_websites = cookie_websites
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        try:
            # Load in cookies for the website
            cookies = read_json_cookies_s3(self.username)
            for website in self.cookie_websites:
                self.driver.get(website)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
        except Exception as e:
            print(str(e))
            print("Error Loading in Cookies")

    def switch(self):
        if self.task == "get_user_data":
            scenario = GetUserInfo(self.driver)
            scenario.user_profile()
        if self.task == "save_user_photos":
            scenario = InstaSavePhoto(self.driver, self.username)
            scenario.download_content()

    def save_cookies(self):
        json.dump(self.driver.get_cookies(), open(self.cookies_local_file_path, "w"))
        final_file_cheker(self.cookies_local_file_path, self.cookies_s3_file_path)

    def load_cookies(self):
        cookies = read_json_cookies_s3(self.username)
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def connect_to_instagram(self):
        self.driver.get(INSTAGRAM_LOGIN)

    def input_username(self):
        self.driver.implicitly_wait(self.small_pause)
        self.driver.find_element(By.XPATH, USERNAME_XPATH).send_keys(self.username)

    def input_password(self):
        self.driver.implicitly_wait(self.small_pause)
        self.driver.find_element(By.XPATH, PASSWORD_XPATH).send_keys(self.password)

    def switch_to_home_tab(self):
        self.driver.implicitly_wait(self.small_pause)
        self.driver.find_element(By.XPATH, HOME_BUTTON).click()

    def turn_off_notification(self):
        try:
            self.driver.find_element(By.XPATH, NOTIFICATIONS_OFF_BUTTON_1).click()
        except Exception as e:
            print(e)
            self.driver.find_element(By.XPATH, NOTIFICATIONS_OFF_BUTTON_2).click()

    def login_button(self):
        self.driver.find_element(By.XPATH, LOGIN_BUTTON).click()

    def login(self):
        """Login to Instagram."""
        if 'Instagram' in self.driver.title:
            print('Already logged in.')
            sleep(1.2)
            self.turn_off_notification()
            self.switch()
        else:
            self.connect_to_instagram()
            self.input_username()
            self.input_password()
            self.login_button()
            self.switch_to_home_tab()
            self.turn_off_notification()
            self.save_cookies()
            self.switch()
