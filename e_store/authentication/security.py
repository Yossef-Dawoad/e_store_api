SPECIAL_CHARS = ["*", "+", "/", "$", "&", "@", "!"]


def verify_pass_strenth(password: str) -> bool:
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    return any(char in SPECIAL_CHARS for char in password)
