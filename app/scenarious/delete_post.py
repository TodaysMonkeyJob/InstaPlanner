from selenium.webdriver.common.by import By

from constans import *


class DeletePost:

    def __init__(self, driver):
        self.driver = driver
        self.small_pause = SMALL_PAUSE
        self.medium_pause = MEDIUM_PAUSE

    def switch_to_user_profile(self):
        switch_step = [USER_PROFILE_SUBMENU, USER_PROFILE_IN_SUBMENU]
        for step in switch_step:
            self.driver.implicitly_wait(self.small_pause)
            self.driver.find_element(By.XPATH, step).click()

    def choose_post_to_delete(self):
        close_button = self.driver.find_element(By.XPATH, FIRST_POST_IN_PROFILE)
        close_button.click()

    def delete_post(self):
        delete_steps = [DELETE_POST_SUBMENU_BUTTON, DELETE_POST_BUTTON_IN_SUBMENU, FINAL_DELETE_POST]
        for step in delete_steps:
            self.driver.implicitly_wait(self.small_pause)
            self.driver.find_element(By.XPATH, step).click()
