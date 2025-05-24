"""Контстаты приложения foodgram."""
MAX_LENGTH_NAME = 256
MAX_LENGTH_SLUG = 50
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_CODE = 40

USERNAME_REGEX = r'^[\w.@+-]+\Z'
SLUG_REGEX = r'^[-a-zA-Z0-9_]+$'

MIN_YEAR_VALUE = -3000
MIN_SCORE_VALUE = 1
MAX_SCORE_VALUE = 10

STR_SHORT_LENGTH = 20
STR_MEDIUM_LENGTH = 50

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"

ROLE_CHOICES = (
    (USER, "Пользователь"),
    (MODERATOR, "Модератор"),
    (ADMIN, "Администратор"),
)
