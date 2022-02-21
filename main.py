from instagram_connection import BrowserConnection

if __name__ == '__main__':
    home_page = BrowserConnection()
    insta = home_page.connect_to_instagram()
    insta.input_username()
    insta.input_password()
    home_tab = insta.log_in()
    home_tab.switch_to_home_tab()
    home_tab.turn_off_notification()
    home_tab.story_cheker()
    home_tab.stories_right_swipe()