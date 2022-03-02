from time import sleep

from selenium.webdriver.common.by import By

from constans import SMALL_PAUSE, MEDIUM_PAUSE, USER_PROFILE_SUBMENU, USER_PROFILE_IN_SUBMENU, \
    FIRST_POST_IN_PROFILE, DELETE_POST_SUBMENU_BUTTON, DELETE_POST_BUTTON_IN_SUBMENU, FINAL_DELETE_POST


class DeletePost:

    def __init__(self, browser):
        self.browser = browser
        self.small_pause = SMALL_PAUSE
        self.medium_pause = MEDIUM_PAUSE

    def switch_to_user_profile(self):
        switch_step = [USER_PROFILE_SUBMENU, USER_PROFILE_IN_SUBMENU]

        for step in switch_step:
            self.browser.implicitly_wait(self.small_pause)
            new_post_button = self.browser.find_element(By.XPATH, step)
            new_post_button.click()


    def choose_post_to_delete(self):
        close_button = self.browser.find_element(By.XPATH, FIRST_POST_IN_PROFILE)
        close_button.click()

    def delete_post(self):
        delete_steps = [DELETE_POST_SUBMENU_BUTTON, DELETE_POST_BUTTON_IN_SUBMENU, FINAL_DELETE_POST]

        for step in delete_steps:
            self.browser.implicitly_wait(self.small_pause)
            delete_post_button = self.browser.find_element(By.XPATH, step)
            delete_post_button.click()

        sleep(50)


