import random
import time

import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from app.s3_help_functions import read_posts_url, final_file_cheker
from constans import *


class InstaSavePhoto:

    def __init__(self, driver, username):
        self.driver = driver
        self.username = username
        self.small_pause = SMALL_PAUSE
        self.posts_urls = list()
        self.post_id_list = list()
        self.img_and_video_src_urls = list()
        self.post_url_path = f'app/tmp/{self.username}_urls.txt'

    def load_user_profile(self):
        self.driver.implicitly_wait(self.small_pause)
        self.driver.get(INSTAGRAM+self.username+'/')

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

    def get_all_posts_urls(self):
        print("User found")
        self.driver.implicitly_wait(self.small_pause)
        loops_count = self.get_loop_count()
        print(f"total loops: {loops_count}")
        for i in range(0, loops_count):
            hrefs = self.driver.find_elements(By.TAG_NAME, 'a')
            hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]
            for href in hrefs:
                if href not in self.posts_urls:
                    self.posts_urls.append(href)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(2, 4))

        with open(self.post_url_path, 'w') as file:
            print(len(set(self.posts_urls)))
            for post_url in self.posts_urls:
                file.write(post_url + "\n")

    def save_helper(self, path, post_id):
        try:
            img_src_url = self.driver.find_element(By.XPATH, path).get_attribute("src")
        except Exception:
            img_src_url = self.driver.find_element(By.XPATH, path).get_attribute("poster")
        self.img_and_video_src_urls.append(img_src_url)
        get_img = requests.get(img_src_url)
        photo_path = f"app/tmp/{post_id}.jpg"
        with open(photo_path, "wb") as img_file:
            img_file.write(get_img.content)
        final_file_cheker(photo_path, f"profile/{self.username}/profile-photo/{post_id}.jpg")

    def new_post_urls(self):
        print("Find active posts")
        try:
            old_post_url = read_posts_url(self.username, f'{self.username}_urls.txt')
        except Exception:
            old_post_url = list()
        new_posts_url = [x for x in self.posts_urls if x not in old_post_url]
        print(f"Found {len(new_posts_url)} new posts")
        final_file_cheker(self.post_url_path, f"profile/{self.username}/{self.username}_urls.txt")
        post_id_path = f'app/tmp/{self.username}_post_id.txt'
        with open(post_id_path, 'w') as file:
            print(len(self.posts_urls))
            for post_ids in self.posts_urls:
                file.write(post_ids.split("/")[-2] + ".jpg\n")
        final_file_cheker(post_id_path, f"profile/{self.username}/{self.username}_post_id.txt")
        return new_posts_url

    def download_userpage_content(self, urls):
        if len(urls) > 0:
            for post_url in urls:
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
                    else:
                        print("Oops, something went wrong")
                        self.img_and_video_src_urls.append(f"{post_url}, no url!")
                    print(f"Content №{len(urls)} from {post_url} successful download!")

                except Exception as e:
                    print(e)
                    self.close_driver()
            self.close_driver()

    def download_content(self):
        #self.load_user_profile()
        self.get_all_posts_urls()
        self.download_userpage_content(self.new_post_urls())
