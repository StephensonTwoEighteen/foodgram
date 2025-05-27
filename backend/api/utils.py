import string
from random import choice, randint
from api.constants import RANDOM_HASH_LENGTH_MAX, RANDOM_HASH_LENGTH_MIN


def generate_hash() -> str:
    """Генерирует случайную строку."""
    return ''.join(
        choice(string.ascii_letters + string.digits)
        for _ in range(randint(RANDOM_HASH_LENGTH_MIN,
                               RANDOM_HASH_LENGTH_MAX))
    )
