from constans import SMALL_PAUSE, HOME_BUTTON, NOTIFICATIONS_OFF_BUTTON, FIRST_STORY, STORY_RIGHT_BUTTON
from selenium.webdriver.common.by import By
from time import sleep


class HomePage:

    def __init__(self, browser):
        self.browser = browser
        self.small_pause = SMALL_PAUSE

    def switch_to_home_tab(self):
        self.browser.implicitly_wait(self.small_pause)
        home_button = self.browser.find_element(By.XPATH, HOME_BUTTON)
        home_button.click()

    def turn_off_notification(self):
        self.browser.implicitly_wait(self.small_pause)
        notifications_off_button = self.browser.find_element(By.XPATH, NOTIFICATIONS_OFF_BUTTON)
        notifications_off_button.click()


    def story_cheker(self):
        self.browser.implicitly_wait(self.small_pause)
        story_button = self.browser.find_element(By.XPATH, FIRST_STORY)
        story_button.click()

    def stories_right_swipe(self):
        while True:
            try:
                self.browser.implicitly_wait(3)
                right_story_button = self.browser.find_element(By.XPATH, STORY_RIGHT_BUTTON)
                right_story_button.click()
            except Exception:
                print("No more stories")
                break
        sleep(50)