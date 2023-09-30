from uuid import uuid4


def create_custom_username(name: str) -> str:
    username = name.split(" ")[0]
    random_digit = uuid4().int % 100
    return f"{username}{random_digit}"


def username_suggestions(name: str) -> list:
    suggestions = []

    for _ in range(2):
        username = name.split(" ")[0]
        random_digit = uuid4().int % 100

        suggestions.append(f"{username}{random_digit}")

    if len(name.split(" ")) > 1:
        for _ in range(2):
            username = name.split(" ")[1]
            random_digit = uuid4().int % 100

            suggestions.append(f"{username}{random_digit}")

        for _ in range(2):
            username = name.split(" ")
            random_digit = uuid4().int % 100

            suggestions.append(f"{username[0]}-{username[1]}{random_digit}")

    return suggestions
