import json

with open("data/messages.json", "r", encoding="utf-8") as file:
    messages = json.load(file)

with open("data/lorem_ipsum.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)


class common:
    HELLO_MESSAGE = messages["hello_message"]
    QUERY_ERROR = messages["query_error"]
    GENERATOR_AGAIN = messages["generator_again"]
    IDEA_MESSAGE = messages["idea_message"]
    SUPPORT_MESSAGE = messages["support_message"]


class users:
    USERS_GENERATOR = messages["users_generator"]
    USERS_GENERATED = messages["users_generated"]
    USERS_GENERATOR_ERROR = messages["users_generator_error"]


class files:
    FILES_GENERATOR = messages["files_generator"]
    FILES_GENERATOR_SIZE = messages["files_generator_size"]
    FILES_GENERATOR_UNIT = messages["files_generator_unit"]
    FILES_EXT = messages["files_ext"]
    FILES_UNIT = messages["files_unit"]
    TEST_FILE = messages["test_file"]
    SUCCESSFULLY_GENERATED = messages["successfully_generated"]
    FILES_GENERATOR_EXT_ERROR = messages["files_generator_ext_error"]
    FILES_GENERATOR_UNIT_ERROR = messages["files_generator_unit_error"]
    FILES_GENERATOR_SIZE_ERROR = messages["files_generator_size_error"]
    FILES_GENERATOR_BIG_FILE = messages["files_generator_big_file"]


class accounts:
    CARDS_GENERATOR = messages["cards_generator"]
    IBAN_GENERATOR = messages["iban_generator"]


class text:
    TEXT_GENERATOR = messages["text_generator"]
    LOREM_IPSUM = json_data["lorem_ipsum"]
    TEXT_GENERATED = messages["text_generated"]
    TEXT_GENERATOR_INT_ERROR = messages["text_generator_int_error"]
    TEXT_GENERATOR_SIZE_ERROR = messages["text_generator_size_error"]
    TEXT_GENERATOR_AGAIN = messages["text_generator_again"]
