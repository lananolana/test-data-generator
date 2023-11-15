"""
config.py - Configuration file for the Telegram bot.

token: Telegram bot API token.
faker: Faker instance for generating fake data.
bot: TeleBot instance for interacting with the Telegram API.
"""

from telebot import TeleBot
from faker import Faker

token = 'TOKEN'
faker = Faker()
bot = TeleBot(token, parse_mode='html')
