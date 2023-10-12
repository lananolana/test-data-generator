# Test Data Generator

Generate test data easily with Telegram bot: random users, credit cards, texts, and files in various formats. This project aims to save the valuable time of QA Engineers and testers by providing an efficient way to prepare test data.

[![Telegram Bot](https://img.shields.io/badge/telegram_bot-090909?style=for-the-badge&logo=telegram)](https://t.me/testdatagenerator_bot)
[![Python](https://img.shields.io/badge/python-090909?style=for-the-badge&logo=python&logoColor=3776AB)](https://www.python.org/downloads/)

> Take a look at this bot before hosting it yourself, and let's improve it together: [Test Data Generator](https://t.me/testdatagenerator_bot) 👈

## Features  🚀

Test Data Generator is a Python-based project using [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) and [Faker](https://github.com/joke2k/faker) package. It provides a convenient way to generate data:

* **Users information.** Full name, mail, password, username, phone, birthdate, and address. Up to 15 users at a time in JSON format.
* **Credit card details.** MasterCard, VISA, AmEx, Maestro, Discover, and JCB.
* **Files in multiple formats.** Any of 20 popular formats from 1 B to 45 MB.
* **Text samples.** Limited only by the Telegram itself: up to 4000 characters.

## Contributing ⭐️

Contributions to this project are welcome! If you'd like to contribute, fork the repository, create a new branch, make your enhancements, and submit a pull request.

If you have any questions, suggestions, or feedback, feel free to [contact me on Telegram](https://t.me/schoegar) or email: `schoegar@gmail.com`

## Installation

If you want to install the project yourself, here's what you need:

1. Install packages using pip (a Python package manager):

    ```bash
    pip install pyTelegramBotAPI
    ```

    ```bash
    pip install Faker
    ```

2. Clone the repo:

    ```bash
    git clone https://github.com/schoegar/test-data-generator/tree/main
    ```

3. Create a Telegram bot using @botFather on Telegram.
4. Obtain your personal `token` from @botFather and insert it into the code.

   ```python
   token = 'TOKEN'
   bot = TeleBot(token, parse_mode = 'html')
   ```
