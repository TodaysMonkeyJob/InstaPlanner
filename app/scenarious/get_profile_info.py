import urllib.request
from time import sleep
import json
from selenium.webdriver.common.by import By

from app.s3_help_functions import final_file_cheker
from constans import *


class GetUserInfo:

    def __init__(self, driver, username):
        self.following = None
        self.followers = None
        self.posts = None
        self.profile_username = username
        self.driver = driver
        self.small_pause = SMALL_PAUSE
        self.medium_pause = MEDIUM_PAUSE

    def user_profile(self):
        self.driver.implicitly_wait(self.small_pause)
        self.driver.get(INSTAGRAM+self.profile_username+'/')
        self.driver.implicitly_wait(self.small_pause)
        self.get_user_info()

    def get_user_info(self):
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
        print("Save Avatar")
        self.driver.implicitly_wait(self.small_pause)
        logo = self.driver.find_element(By.XPATH, PROFILE_IMAGE)
        src = logo.get_attribute('src')
        urllib.request.urlretrieve(src, f"app/tmp/{self.profile_username}.jpg")
        final_file_cheker(f"app/tmp/{self.profile_username}.jpg",
                          f'profile/{self.profile_username}/profile-photo/{self.profile_username}.jpg')
        sleep(3)


    def save_user_info(self):
        print("Save user data")
        user_info = {'username': self.profile_username, 'posts': self.posts,
                     'followers': self.followers, 'following': self.following}
        with open(f'app/tmp/{self.profile_username}.json', 'w') as file:
            json.dump(user_info, file)
        final_file_cheker(f'app/tmp/{self.profile_username}.json',
                          f'profile/{self.profile_username}/{self.profile_username}.json')
