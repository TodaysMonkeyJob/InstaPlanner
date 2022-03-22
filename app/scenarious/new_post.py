from time import sleep

from selenium.webdriver.common.by import By

from app.s3_help_functions import download_from_s3
from constans import *


class NewPost:

    def __init__(self, driver, username):
        self.driver = driver
        self.username = username
        self.new_photo = TEST_PHOTO
        self.small_pause = SMALL_PAUSE
        self.medium_pause = MEDIUM_PAUSE

    def close_driver(self):
        self.driver.close()
        self.driver.quit()

    def switch_to_new_post_tab(self):
        self.driver.implicitly_wait(self.small_pause)
        self.driver.find_element(By.XPATH, NEW_POST).click()
        self.add_new_photo()

    def add_new_photo(self):
        download_from_s3('test-photo/CK1VR7wlUdq.jpg')
        self.set_photo()
        sleep(1.2)
        self.add_tag_to_photo()
        self.move_forward()
        sleep(3)
        self.close_driver()

    def set_photo(self):
        try:
            self.driver.implicitly_wait(self.medium_pause)
            add_photo_button = self.driver.find_element(By.XPATH, SELECT_PHOTO)
            add_photo_button.send_keys(self.new_photo)
        except Exception as exception:
            print(exception)
        self.move_forward()
        self.move_forward()


    def add_tag_to_photo(self):
        self.driver.implicitly_wait(self.small_pause)
        self.driver.find_element(By.XPATH, ADD_PHOTO_TAG_FIELD).click()
        self.driver.implicitly_wait(self.small_pause)
        self.driver.find_element(By.XPATH, ADD_PHOTO_TAG_INPUT).send_keys("blck_n_brwn")
        self.driver.implicitly_wait(self.small_pause)
        self.driver.find_element(By.XPATH, ADD_PHOTO_TAG_SELECT).click()

    def move_forward(self):
        self.driver.implicitly_wait(self.small_pause)
        try:
            self.driver.find_element(By.XPATH, NEW_POST_NEXT_1).click()
        except Exception:
            self.driver.find_element(By.XPATH, NEW_POST_NEXT_2).click()

    def close_post_sharing(self):
        try:
            self.driver.find_element(By.XPATH, CLOSE_POST_SHARING).click()
        except Exception as e:
            print(e)
