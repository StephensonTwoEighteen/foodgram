from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.constants import (
    COOKING_TIME_MAX,
    COOKING_TIME_MIN,
    INGREDIENT_NAME_MAX_LEENGTH,
    MAX_MEASUREMENT_INGREDIENT_UNIT,
    RANDOM_HASH_LENGTH_MAX,
    RECIPE_INGREDIENT_AMOUT_MAX,
    RECIPE_INGREDIENT_AMOUT_MIN,
    RECIPE_NAME_MAX_LENGTH,
    TAG_NAME_MAX_LENGTH,
    USER_EMAIL_MAX_LENGTH,
    USER_NAME_MAX_LENGTH
)
from api.utils import generate_hash


class User(AbstractUser):
    email = models.EmailField(max_length=USER_EMAIL_MAX_LENGTH,
                              unique=True,
                              verbose_name='Почта')
    username = models.CharField(max_length=USER_NAME_MAX_LENGTH,
                                unique=True,
                                verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=USER_NAME_MAX_LENGTH,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=USER_NAME_MAX_LENGTH,
                                 verbose_name='Фамилия')
    is_subscribed = models.BooleanField(default=False,
                                        verbose_name='Есть ли подписка')
    avatar = models.ImageField(upload_to='users/',
                               blank=True,
                               null=True,
                               verbose_name='')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=TAG_NAME_MAX_LENGTH,
                            unique=True,
                            verbose_name='Название')
    slug = models.SlugField(max_length=TAG_NAME_MAX_LENGTH,
                            unique=True,
                            allow_unicode=True,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=INGREDIENT_NAME_MAX_LEENGTH,
                            verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=MAX_MEASUREMENT_INGREDIENT_UNIT,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        null=False,
        verbose_name='Автор'
    )
    name = models.CharField(max_length=RECIPE_NAME_MAX_LENGTH,
                            verbose_name='Наименование')
    image = models.ImageField(upload_to='recipes/',
                              verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(COOKING_TIME_MIN),
                    MaxValueValidator(COOKING_TIME_MAX)],
        verbose_name='Время приготовления'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Тэги')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты'
    )
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    short_link = models.SlugField(
        max_length=RANDOM_HASH_LENGTH_MAX,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Короткая ссылка'
    )

    def save(self, *args, **kwargs):
        if not self.short_link:
            self.short_link = generate_hash()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(RECIPE_INGREDIENT_AMOUT_MIN),
                    MaxValueValidator(RECIPE_INGREDIENT_AMOUT_MAX)],
        verbose_name='Сумма'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        ordering = ('ingredient',)

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'{self.user} {self.author}'


class LinkMapped(models.Model):
    url_hash = models.CharField(max_length=RANDOM_HASH_LENGTH_MAX,
                                unique=True,
                                verbose_name='Хэш урла')
    original_url = models.CharField(max_length=RANDOM_HASH_LENGTH_MAX,
                                    verbose_name='Оригинальный урл')

    def save(self, *args, **kwargs):
        if not self.url_hash:
            self.url_hash = generate_hash()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Сокращенная ссылка'
        verbose_name_plural = 'Сокращенные ссылки'

    def __str__(self):
        return f"{self.url_hash} -> {self.original_url}"
