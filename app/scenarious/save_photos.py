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
        self.post_id_list = list()
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
        if os.path.exists(f"app/static/{self.username}"):
            print("Folder already exist!")
        else:
            os.mkdir(f"app/static/{self.username}")

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

        with open(f'app/static/{self.username}/{self.username}.txt', 'a') as file:
            for post_url in self.posts_urls:
                file.write(post_url + "\n")

    def save_helper(self, path, post_id):
        try:
            img_src_url = self.driver.find_element(By.XPATH, path).get_attribute("src")
        except Exception:
            img_src_url = self.driver.find_element(By.XPATH, path).get_attribute("poster")
        self.img_and_video_src_urls.append(img_src_url)
        get_img = requests.get(img_src_url)
        with open(f"app/static/{self.username}/{post_id}.jpg", "wb") as img_file:
            img_file.write(get_img.content)

    def download_userpage_content(self, urls):
        if len(urls) > 0:
            unique = list()
            for post_url in urls:
                if post_url not in unique:
                    unique.append(post_url)
                    try:
                        self.driver.get(post_url)
                        post_id = post_url.split("/")[-2]
                        self.post_id_list.append(post_id)
                        if self.xpath_exists(PROFILE_PHOTO_POSTS_1):
                            self.save_helper(PROFILE_PHOTO_POSTS_1, post_id)
                        elif self.xpath_exists(PROFILE_PHOTO_POSTS_2):
                            self.save_helper(PROFILE_PHOTO_POSTS_2, post_id)
                        elif self.xpath_exists(PROFILE_PHOTO_POSTS_3):
                            self.save_helper(PROFILE_PHOTO_POSTS_3, post_id)
                        elif self.xpath_exists(PROFILE_VIDEO_POSTS_1):
                            self.save_helper(PROFILE_VIDEO_POSTS_1, post_id)
                        elif self.xpath_exists(PROFILE_VIDEO_POSTS_2):
                            self.save_helper(PROFILE_VIDEO_POSTS_2, post_id)

                        # elif self.xpath_exists(PROFILE_VIDEO_POSTS_1):
                        #     video_src_url = self.driver.find_element(By.XPATH, PROFILE_VIDEO_POSTS_1).get_attribute("src")
                        #     self.img_and_video_src_urls.append(video_src_url)
                        #     get_video = requests.get(video_src_url, stream=True)
                        #     with open(f"app/static/{self.username}/{self.username}_{post_id}_video.mp4", "wb") as video_file:
                        #         for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                        #             if chunk:
                        #                 video_file.write(chunk)
                        #
                        # elif self.xpath_exists(PROFILE_VIDEO_POSTS_2):
                        #     video_src_url = self.driver.find_element(By.XPATH, PROFILE_VIDEO_POSTS_2).get_attribute("src")
                        #     self.img_and_video_src_urls.append(video_src_url)
                        #     get_video = requests.get(video_src_url, stream=True)
                        #     with open(f"app/static/{self.username}/{self.username}_{post_id}_video.mp4", "wb") as video_file:
                        #         for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                        #             if chunk:
                        #                 video_file.write(chunk)
                        #     time.sleep(10)

                        else:
                            print("Oops, something went wrong")
                            self.img_and_video_src_urls.append(f"{post_url}, no url!")
                            self.posts_urls_extra.append(post_url)
                        print(f"Content №{len(unique)} from {post_url} successful download!")

                    except Exception as e:
                        print(e)
                        self.close_driver()
            self.close_driver()

            with open(f'app/static/{self.username}/{self.username}_img_and_video_src_urls.txt', 'a') as file:
                for i in self.img_and_video_src_urls:
                    file.write(i + "\n")

            with open(f'app/static/{self.username}/{self.username}_post_id.txt', 'a') as file:
                for post_ids in self.post_id_list:
                    file.write(post_ids + ".jpg\n")

    def download_content(self):
        self.load_user_profile()
        self.create_profile_folder()
        self.get_all_posts_urls()
        self.download_userpage_content(self.posts_urls)
