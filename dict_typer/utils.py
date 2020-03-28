from keyword import iskeyword


def is_valid_key(key: str) -> bool:
    if iskeyword(key):
        return False
    return key.isidentifier()


def key_to_class_name(key: str) -> str:
    return "".join(part[0].upper() + part[1:] for part in key.split("_"))
