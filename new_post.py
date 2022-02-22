from time import sleep

from selenium.webdriver.common.by import By

from constans import SMALL_PAUSE, NEW_POST, SELECT_PHOTO, MEDIUM_PAUSE, NEW_POST_NEXT, NEW_POST_SHARE


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
        try:
            self.browser.implicitly_wait(self.medium_pause)
            add_photo_button = self.browser.find_element(By.XPATH, SELECT_PHOTO)
            add_photo_button.send_keys('/home/oleh/PyProjects/instaPlanner/test_photos/IMG_1355.JPG')
        except Exception as exception:
            print(exception)
        # import ipdb;
        # ipdb.set_trace()

        self.browser.implicitly_wait(self.medium_pause)
        next_photo_button = self.browser.find_element(By.XPATH, NEW_POST_NEXT)
        next_photo_button.click()
        next_photo_button = self.browser.find_element(By.XPATH, NEW_POST_NEXT)
        next_photo_button.click()
        sleep(2)
        share_photo_button = self.browser.find_element(By.XPATH, NEW_POST_SHARE)
        share_photo_button.click()
        sleep(50)

