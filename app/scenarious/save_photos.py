import os
import random
import time

import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from constans import *


class InstaSavePhoto:

    def __init__(self, driver, username):
        self.driver = driver
        self.username = username
        self.small_pause = SMALL_PAUSE
        self.posts_urls = list()
        self.posts_urls_extra = list()
        self.img_and_video_src_urls = list()

    def load_user_profile(self):
        switch_step = [USER_PROFILE_SUBMENU, USER_PROFILE_IN_SUBMENU]
        for step in switch_step:
            self.driver.implicitly_wait(self.small_pause)
            self.driver.find_element(By.XPATH, step).click()

    def xpath_exists(self, path):
        try:
            self.driver.find_element(By.XPATH, path)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    def close_driver(self):
        self.driver.close()
        self.driver.quit()

    def get_loop_count(self):
        self.driver.implicitly_wait(self.small_pause)
        posts_count = int(self.driver.find_element(By.XPATH, PROFILE_POSTS).text)
        return int((posts_count / 12) + (posts_count % 12 > 0))

    def create_profile_folder(self):
        if os.path.exists(f"{self.username}"):
            print("Folder already exist!")
        else:
            os.mkdir(self.username)

    def get_all_posts_urls(self):
        print("User found")

        loops_count = self.get_loop_count()
        for i in range(0, loops_count):
            hrefs = self.driver.find_elements(By.TAG_NAME, 'a')
            print(hrefs)
            hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

            for href in hrefs:
                self.posts_urls.append(href)

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(2, 4))

        self.create_profile_folder()
        with open(f'{self.username}/{self.username}.txt', 'a') as file:
            for post_url in self.posts_urls:
                file.write(post_url + "\n")

    def download_userpage_content(self, urls):
        if len(urls) > 0:
            for post_url in urls:
                try:
                    time.sleep(4)
                    self.driver.get(post_url)
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(PROFILE_PHOTO_POSTS):
                        img_src_url = self.driver.find_element(By.XPATH, PROFILE_PHOTO_POSTS).get_attribute("src")
                        self.img_and_video_src_urls.append(img_src_url)

                        get_img = requests.get(img_src_url)
                        with open(f"{self.username}/{self.username}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exists(PROFILE_VIDEO_POSTS):
                        video_src_url = self.driver.find_element(By.XPATH, PROFILE_VIDEO_POSTS).get_attribute("src")
                        self.img_and_video_src_urls.append(video_src_url)
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f"{self.username}/{self.username}_{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)

                    else:
                        print("Oops, something went wrong")
                        self.img_and_video_src_urls.append(f"{post_url}, no url!")
                        self.posts_urls_extra.append(post_url)
                    print(f"Content from {post_url} successful download!")

                except Exception as e:
                    print(e)
                    self.close_driver()
            self.close_driver()

            with open(f'{self.username}/{self.username}_img_and_video_src_urls.txt', 'a') as file:
                for i in self.img_and_video_src_urls:
                    file.write(i + "\n")

    def download_content(self):
        self.load_user_profile()
        self.get_all_posts_urls()
        self.download_userpage_content(self.posts_urls)
        self.download_userpage_content(self.posts_urls_extra)
