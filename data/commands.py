from generator.bot import Generator


class Command:
    def __init__(self, command, button, description, handler):
        self.command = command
        self.button = button
        self.description = description
        self.handler = handler


COMMANDS = [
    Command("/start", "Back to start", "Start command", Generator.welcome),
    Command("/users", "Users", "Generate user data", "users_handler"),
    Command("/file", "File", "Generate files", "file_handler"),
    Command("/card", "Credit card", "Generate bank cards", "card_handler"),
    Command("/iban", "IBAN", "Generate IBANs", "iban_handler"),
    Command("/text", "Text", "Generate text", "text_handler"),
    Command(
        "/feedback", "💬 Share feedback", "Share feedback", "feedback_handler"
    )
]
