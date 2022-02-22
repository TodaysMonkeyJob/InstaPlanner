from time import sleep

from selenium.webdriver.common.by import By

from constans import SMALL_PAUSE, NEW_POST, SELECT_PHOTO, MEDIUM_PAUSE, NEW_POST_NEXT, NEW_POST_SHARE, TEST_PHOTO, \
    CLOSE_POST_SHARING


class NewPost:

    def __init__(self, browser):
        self.browser = browser
        self.small_pause = SMALL_PAUSE
        self.medium_pause = MEDIUM_PAUSE

    def switch_to_new_post_tab(self):
        self.browser.implicitly_wait(self.small_pause)
        new_post_button = self.browser.find_element(By.XPATH, NEW_POST)
        new_post_button.click()

    def add_new_photo(self):
        self.set_photo()
        sleep(2)
        self.share_photo()
        sleep(5)
        self.close_post_sharing()

    def set_photo(self):
        try:
            self.browser.implicitly_wait(self.medium_pause)
            add_photo_button = self.browser.find_element(By.XPATH, SELECT_PHOTO)
            add_photo_button.send_keys(TEST_PHOTO)
        except Exception as exception:
            print(exception)
        next_photo_button = self.browser.find_element(By.XPATH, NEW_POST_NEXT)
        next_photo_button.click()
        next_photo_button = self.browser.find_element(By.XPATH, NEW_POST_NEXT)
        next_photo_button.click()

    def share_photo(self):
        share_photo_button = self.browser.find_element(By.XPATH, NEW_POST_SHARE)
        share_photo_button.click()

    def close_post_sharing(self):
        close_button = self.browser.find_element(By.XPATH, CLOSE_POST_SHARING)
        close_button.click()
