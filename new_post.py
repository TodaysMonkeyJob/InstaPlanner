from time import sleep

from selenium.webdriver.common.by import By

from constans import SMALL_PAUSE, NEW_POST, SELECT_PHOTO, MEDIUM_PAUSE, NEW_POST_NEXT, NEW_POST_SHARE, TEST_PHOTO, \
    CLOSE_POST_SHARING, ADD_PHOTO_TAG_FIELD, ADD_PHOTO_TAG_INPUT, ADD_PHOTO_TAG_SELECT
from delete_post import DeletePost


class NewPost:

    def __init__(self, browser):
        self.browser = browser
        self.new_photo = TEST_PHOTO
        self.small_pause = SMALL_PAUSE
        self.medium_pause = MEDIUM_PAUSE

    def switch_to_new_post_tab(self):
        self.browser.implicitly_wait(self.small_pause)
        new_post_button = self.browser.find_element(By.XPATH, NEW_POST)
        new_post_button.click()

    def add_new_photo(self):
        self.set_photo()
        sleep(2)
        self.add_tag_to_photo()
        self.share_photo()
        sleep(7)
        self.close_post_sharing()

    def set_photo(self):
        try:
            self.browser.implicitly_wait(self.medium_pause)
            add_photo_button = self.browser.find_element(By.XPATH, SELECT_PHOTO)
            add_photo_button.send_keys(self.new_photo)
        except Exception as exception:
            print(exception)
        next_photo_button = self.browser.find_element(By.XPATH, NEW_POST_NEXT)
        next_photo_button.click()
        next_photo_button = self.browser.find_element(By.XPATH, NEW_POST_NEXT)
        next_photo_button.click()

    def add_tag_to_photo(self):
        self.browser.implicitly_wait(self.small_pause)
        add_tag = self.browser.find_element(By.XPATH, ADD_PHOTO_TAG_FIELD)
        add_tag.click()
        self.browser.implicitly_wait(self.small_pause)
        add_tag = self.browser.find_element(By.XPATH, ADD_PHOTO_TAG_INPUT)
        add_tag.send_keys("blck_n_brwn")
        self.browser.implicitly_wait(self.small_pause)
        add_tag = self.browser.find_element(By.XPATH, ADD_PHOTO_TAG_SELECT)
        add_tag.click()



    def share_photo(self):
        share_photo_button = self.browser.find_element(By.XPATH, NEW_POST_SHARE)
        share_photo_button.click()

    def close_post_sharing(self):
        try:
            close_button = self.browser.find_element(By.XPATH, CLOSE_POST_SHARING)
            close_button.click()
        except Exception:
            pass
        return DeletePost(self.browser)
