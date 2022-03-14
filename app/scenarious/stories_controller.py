from constans import *
from selenium.webdriver.common.by import By


class Stories:

    def __init__(self, driver):
        self.driver = driver
        self.small_pause = SMALL_PAUSE

    def story_cheker(self):
        self.driver.implicitly_wait(self.small_pause)
        story_button = self.driver.find_element(By.XPATH, FIRST_STORY)
        story_button.click()

    def stories_right_swipe(self):
        while True:
            try:
                self.driver.implicitly_wait(3)
                right_story_button = self.driver.find_element(By.XPATH, STORY_RIGHT_BUTTON)
                right_story_button.click()
            except Exception:
                print("No more stories")
                break