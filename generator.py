import json
from handlers import (
    users_handler,
    card_handler,
    iban_handler,
    file_handler,
    text_handler,
    feedback_handler
)
from data.keyboard_objects import requests
from config import bot, commands
from telebot import types

# Custom commands
bot.set_my_commands([types.BotCommand(command[0], command[1])
                     for command in commands])


def load_messages():
    with open("data/messages.json", "r", encoding="utf-8") as file:
        messages = json.load(file)
    return messages


def initialize_messages():
    global messages
    messages = load_messages()


@bot.message_handler(commands=['start'])
def welcome(message):
    # Getting the Telegram username
    username = message.from_user.first_name

    # Main keyboard object
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*requests, row_width=2)

    # Sending reply for start command handler with keyboard object
    reply = f"Hey, <b>{username}</b>!" + messages["hello_message"]
    bot.send_message(message.chat.id, reply, reply_markup=markup)

    # Register the transition to the next step
    bot.register_next_step_handler(reply, check_request)


def check_request(message):
    match message.text:
        case '/start':
            welcome(message)
        case 'Users' | '/users':
            users_handler.users_handler(message)
        case 'File' | '/file':
            file_handler.file_handler(message)
        case 'Credit card' | '/card':
            card_handler.card_handler(message)
        case 'IBAN' | '/iban':
            iban_handler.iban_handler(message)
        case 'Text' | '/text':
            text_handler.text_handler(message)
        case '💬 Share feedback' | '/feedback':
            feedback_handler.feedback_handler(message)
        case _:
            reply = bot.send_message(message.chat.id, messages["query_error"])
            bot.register_next_step_handler(reply, check_request)


# Main function, launching the polling bot
def main():
    bot.infinity_polling()


# The special construct for the program entry point (main function)
if __name__ == '__main__':
    main()
