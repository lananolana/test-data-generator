from telebot import TeleBot
from faker import Faker

token = 'TOKEN'
faker = Faker()
bot = TeleBot(token, parse_mode='html')
