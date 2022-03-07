import urllib.request
from time import sleep
import json

from selenium.webdriver.common.by import By

from constans import SMALL_PAUSE, MEDIUM_PAUSE, USER_PROFILE_SUBMENU, USER_PROFILE_IN_SUBMENU, \
    FIRST_POST_IN_PROFILE, DELETE_POST_SUBMENU_BUTTON, DELETE_POST_BUTTON_IN_SUBMENU, FINAL_DELETE_POST, PROFILE_IMAGE, \
    PROFILE_USERNAME, PROFILE_POSTS, PROFILE_FOLLOWERS, PROFILE_FOLLOWING


class GetUserInfo:

    def __init__(self, browser):
        self.following = None
        self.followers = None
        self.posts = None
        self.profile_username = None
        self.browser = browser
        self.small_pause = SMALL_PAUSE
        self.medium_pause = MEDIUM_PAUSE

    def switch_to_user_profile(self):
        switch_step = [USER_PROFILE_SUBMENU, USER_PROFILE_IN_SUBMENU]

        for step in switch_step:
            self.browser.implicitly_wait(self.small_pause)
            new_post_button = self.browser.find_element(By.XPATH, step)
            new_post_button.click()

    def get_user_info(self):
        self.browser.implicitly_wait(self.small_pause)
        self.profile_username = self.browser.find_element(By.XPATH, PROFILE_USERNAME).text
        self.posts = self.browser.find_element(By.XPATH, PROFILE_POSTS).text
        self.followers = self.browser.find_element(By.XPATH, PROFILE_FOLLOWERS).text
        self.following = self.browser.find_element(By.XPATH, PROFILE_FOLLOWING).text
        self.save_user_info()
        self.save_avatar()

    def save_avatar(self):
        self.browser.implicitly_wait(self.small_pause)
        logo = self.browser.find_element(By.XPATH, PROFILE_IMAGE)
        src = logo.get_attribute('src')
        urllib.request.urlretrieve(src, f"/home/oleh/PyProjects/instaPlanner/app/static/img/{self.profile_username}.jpg")
        sleep(30)

    def save_user_info(self):
        user_info = {'username': self.profile_username, 'posts': self.posts,
                     'followers': self.followers, 'following': self.following}
        with open(f'/home/oleh/PyProjects/instaPlanner/app/json_data/{self.profile_username}.json', 'w') as file:
            json.dump(user_info, file)
