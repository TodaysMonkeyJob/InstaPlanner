import urllib.request
from time import sleep
import json
from selenium.webdriver.common.by import By
from constans import *


class GetUserInfo:

    def __init__(self, driver):
        self.following = None
        self.followers = None
        self.posts = None
        self.profile_username = None
        self.driver = driver
        self.small_pause = SMALL_PAUSE
        self.medium_pause = MEDIUM_PAUSE

    def user_profile(self):
        switch_step = [USER_PROFILE_SUBMENU, USER_PROFILE_IN_SUBMENU]
        for step in switch_step:
            self.driver.implicitly_wait(self.small_pause)
            self.driver.find_element(By.XPATH, step).click()
        self.get_user_info()

    def get_user_info(self):
        self.driver.implicitly_wait(self.small_pause)
        try:
            self.profile_username = self.driver.find_element(By.XPATH, PROFILE_USERNAME_H1).text
        except Exception:
            self.profile_username = self.driver.find_element(By.XPATH, PROFILE_USERNAME_H2).text
        self.posts = self.driver.find_element(By.XPATH, PROFILE_POSTS).text
        self.followers = self.driver.find_element(By.XPATH, PROFILE_FOLLOWERS).text
        self.following = self.driver.find_element(By.XPATH, PROFILE_FOLLOWING).text
        self.save_user_info()
        self.save_avatar()

    def save_avatar(self):
        self.driver.implicitly_wait(self.small_pause)
        logo = self.driver.find_element(By.XPATH, PROFILE_IMAGE)
        src = logo.get_attribute('src')
        urllib.request.urlretrieve(src, f"app/static/img/{self.profile_username}.jpg")
        sleep(5)


    def save_user_info(self):
        user_info = {'username': self.profile_username, 'posts': self.posts,
                     'followers': self.followers, 'following': self.following}
        with open(f'app/info_data/{self.profile_username}.json', 'w') as file:
            json.dump(user_info, file)
