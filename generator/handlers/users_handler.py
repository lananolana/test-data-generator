import json
from config import faker, bot, users_objects
from utils.bot_handler import BotHandler
from utils.constants import common, users
from secrets import token_urlsafe


@bot.message_handler(commands=['users'])
def users_handler(message):
    users_markup = BotHandler.markup_setup(users_objects.users, 2)
    BotHandler.add_back_to_start_button(users_markup)

    BotHandler.send_message(
        message, users.USERS_GENERATOR,
        markup=users_markup, next_handler=users_number
    )


def users_number(message):
    payload_len = users_objects.payload_lens.get(message.text)

    if payload_len:
        users_generator(payload_len, message)
    elif (message.text.isdigit() and 0 < int(message.text) <= 15):
        payload_len = int(message.text)
        users_generator(payload_len, message)
    elif message.text.isdigit():
        BotHandler.error(
            message, users.USERS_GENERATOR_ERROR, None, users_number
        )
    else:
        BotHandler.are_back_buttons(
            message, None, common.QUERY_ERROR, None, users_number
        )


def users_generator(payload_len, message):
    # Generate test data for the selected number of users
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'{faker.msisdn()[4:]}'
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    # Serialise the data into a string
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str)

    users_sender(payload_len, payload_str, message)


def users_sender(payload_len, payload_str, message):
    BotHandler.send_message(
        message, {payload_len}, users.USERS_GENERATED,
        f"<code>{payload_str}</code>"
    )
    BotHandler.send_message(
        message, common.GENERATOR_AGAIN, next_handler=users_number
    )
