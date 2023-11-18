"""
main.py - Main script to run the Telegram bot.

test_bot: An instance of the bot used for testing purposes.
"""

from generator.bot import Generator

if __name__ == '__main__':
    test_bot = Generator()
    test_bot.run()
