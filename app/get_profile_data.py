from app.scenarious.instagram_connection import BrowserConnection

def main(name, password):
    home_page = BrowserConnection(name, password)
    insta = home_page.connect_to_instagram()
    insta.input_username()
    insta.input_password()
    home_tab = insta.log_in()
    home_tab.switch_to_user_profile()
    home_tab.get_user_info()


if __name__ == '__main__':
    main()