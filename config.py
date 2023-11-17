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
requests = [
    'Users',
    'File',
    'Credit card',
    'IBAN',
    'Text',
    '💬 Share feedback'
]


class users_objects:
    users = ['1️⃣', '3️⃣', '5️⃣', '🔟']
    payload_lens = {
        '1️⃣': 1,
        '3️⃣': 3,
        '5️⃣': 5,
        '🔟': 10
    }


class cards_objects:
    cards = ['MasterCard', 'VISA', 'AmEx', 'Maestro', 'Discover', 'JCB']
    card_types = {
        'VISA': 'visa',
        'MasterCard': 'mastercard',
        'Maestro': 'maestro',
        'JCB': 'jcb',
        'AmEx': 'amex',
        'Discover': 'discover'
    }


class files_objects:
    formats = [
        '.jpg', '.png', '.svg', '.gif', '.ico', '.mp4', '.avi',
        '.webm', '.doc', '.docx', '.xls', '.xlsx', '.txt', '.pdf',
        '.css', '.html', '.js', '.json', '.zip', '.rar'
    ]
    units = ["B", "KB", "MB"]


class iban_objects:
    iban_countries = ['🇬🇧 GB', '🇧🇪 BE', '🇩🇪 DE', '🇫🇷 FR', '🇳🇱 NL', '🇪🇸 ES']
    country_codes = {
        '🇬🇧 GB': 'gb',
        '🇧🇪 BE': 'be',
        '🇩🇪 DE': 'de',
        '🇫🇷 FR': 'fr',
        '🇳🇱 NL': 'nl',
        '🇪🇸 ES': 'es'
    }
    bank_codes = {
        'be': ["{:03}".format(i) for i in range(1000)],
        'de': [
            "10010010", "11010101", "37040044", "50010517", "10011001",
            "10040000", "10050000", "10070024", "12030000", "20030000",
            "20040000", "20050550", "20070000", "20070024", "30020900",
            "30030880", "30060601", "37050198", "50010517", "50040000",
            "50050201", "50070010", "50110800", "51230800", "60050101",
            "60070070", "70010080", "70020270", "70070010", "70070024",
            "70150000", "85050300"
        ],
        'fr': [
            "3000100794", "3000400003", "3000600001", "1010700101",
            "1131500001", "3000203253", "3005600927", "1180800910",
            "1001100020", "3007602082", "1441000001", "1254802998",
            "3000700011", "4255900001", "3008746642", "2004101005"
        ],
        'nl': [
            "ABNA", "RBOS", "AHBK", "ARBN", "AEGO", "AENV", "AKBK", "AMSC",
            "STOL", "ANDL", "ABPT", "ARAM", "AZLH", "INSI", "BKMG", "BOFA",
            "BKCH", "BOFA", "BKCH", "BOFS", "BOTK", "BICK", "BNPA", "CGGV",
            "CITC", "CITI", "COBA", "DRES", "FBHL", "ISBK", "BCIT", "INGI",
            "BBRU", "INGB", "HSBC", "HABB", "ARTE", "UGBI", "FRBK", "FTSI",
            "NECI", "ECLN", "INND", "EMCF", "TEBU", "DSTA", "MIFI", "DSSB",
            "DEUT", "DLBK", "DLIM", "DAIX", "HBUA", "EQUI", "DHBN"
        ],
        'es': [
            "2100", "1560", "8840", "1575", "1480", "6715", "8806", "6709",
            "6719", "8769", "8512", "8596", "1557", "2103", "0226", "1491",
            "6721", "4784", "1487", "1570", "1573", "8836", "0216", "6724",
            "1572", "8838", "1578", "0108", "8816", "1551", "1490", "8833",
            "8795", "6705", "8813", "8845", "4797", "0036", "8906", "0224",
            "0242", "3138", "1583", "0083", "1508", "6713", "6707", "6722",
            "1568", "0073", "1565", "8814", "1577", "0133", "1479", "1563",
            "1544", "0160", "6720", "6723", "1559", "0244", "1552"
        ]
    }
    acc_num_len = {
        'be': 7,
        'de': 8,
        'fr': 5,
        'nl': 8,
        'es': 10
    }
