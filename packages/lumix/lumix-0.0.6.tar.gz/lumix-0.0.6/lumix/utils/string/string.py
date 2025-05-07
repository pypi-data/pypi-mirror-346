import re
import random
import string


__all__ = [
    "random_string",
    "drop_multi_mark",
]


def random_string(length: int = 10) -> str:
    """"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def drop_multi_mark(text: str, mark: str = "\n") -> str:
    """"""
    cleaned_text = re.sub(f'({mark}){{3,}}', f'{mark}{mark}', text)
    return cleaned_text
