import json

from handlers import (
    users_handler,
    card_handler,
    file_handler,
    text_handler,
    feedback_handler
)
from config import bot, messages, requests
from telebot import types

# Custom commands
bot.set_my_commands([types.BotCommand(
    '/start',
    '/users',
    '/file',
    '/card',
    '/text',
    '/feedback'
)])


def load_messages():
    with open("messages.json", "r", encoding="utf-8") as file:
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
    if message.text == '/start':
        welcome(message)
    elif message.text == ('Users' or '/users'):
        users_handler.users_handler(message)
    elif message.text == ('File' or '/file'):
        file_handler.file_handler(message)
    elif message.text == ('Credit card' or '/card'):
        card_handler.card_handler(message)
    elif message.text == ('Text' or '/text'):
        text_handler(message)
    elif message.text == ('💬 Share feedback' or 'feedback'):
        feedback_handler.feedback_handler(message)
    else:
        reply = bot.send_message(message.chat.id, messages["query_error"])
        bot.register_next_step_handler(reply, check_request)


# Main function, launching the polling bot
def main():
    bot.infinity_polling()


# The special construct for the program entry point (main function)
if __name__ == '__main__':
    main()
