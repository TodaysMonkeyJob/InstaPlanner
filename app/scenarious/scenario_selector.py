from app.scenarious.instagram_connection import IntaLogin


def launch_scenario(username, password, task):
    bot = IntaLogin(username, password, task)
    bot.login()
