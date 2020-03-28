from keyword import iskeyword


def is_valid_key(key: str) -> bool:
    if iskeyword(key):
        return False
    return key.isidentifier()
