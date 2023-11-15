"""
main.py - Main script to run the Telegram bot.

test_bot: An instance of the bot used for testing purposes.
"""


from generator import bot

if __name__ == '__main__':
    test_bot = bot()
    test_bot.run()
