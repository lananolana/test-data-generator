"""
main.py - Main script to run the Telegram bot.
"""

from generator.bot import Generator

if __name__ == '__main__':
    bot = Generator()
    bot.run()
