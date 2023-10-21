from telebot import TeleBot
from faker import Faker

token = 'TOKEN'
faker = Faker()
bot = TeleBot(token, parse_mode='html')
messages = {}

# Main keyboard objects
requests = ['Users', 'File', 'Credit card', 'IBAN', 'Text', '💬 Share feedback']
users = ['1️⃣', '3️⃣', '5️⃣', '🔟']
cards = ['MasterCard', 'VISA', 'AmEx', 'Maestro', 'Discover', 'JCB']
iban_countries = ['GB 🇬🇧', 'BE 🇧🇪', 'GE 🇩🇪', 'FR 🇫🇷', 'NL 🇳🇱', 'PT 🇵🇹']
formats = ['.jpg', '.png', '.svg', '.gif', '.ico', '.mp4', '.avi',
           '.webm', '.doc', '.docx', '.xls', '.xlsx', '.txt',
           '.pdf', '.css', '.html', '.js', '.json', '.zip', '.rar']
