import re

def is_translatable(message):
    if not message.content.strip():
        return False
    if message.author.bot:
        return False
    if message.content.startswith(("/", "!", ".")):
        return False
    if re.match(r"^[\W_]+$", message.content):  # emojis or symbols only
        return False
    if re.search(r"http[s]?://", message.content):  # contains link
        return False
    return True
