from telebot import TeleBot
from faker import Faker

token = 'TOKEN'
faker = Faker()
bot = TeleBot(token, parse_mode='html')

commands = [
    ("/start", "Start command"),
    ("/users", "Generate user data"),
    ("/file", "Generate files"),
    ("/card", "Generate bank cards"),
    ("/iban", "Generate IBANs"),
    ("/text", "Generate text"),
    ("/feedback", "Leave feedback")
]
