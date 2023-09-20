from uuid import uuid4

def create_custom_username(name: str) -> str:
    username = name.split(" ")[0]
    random_digit = uuid4().int % 100
    return f"{username}{random_digit}"