from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from core.constants import (DEFAULT_AMOUNT_INGREDIENT_INREC,
                            MAX_COOKING_TIME_REC, MAX_LENGTH_COLOR_TAG,
                            MAX_LENGTH_MEASUREMENT_UNIT_ING,
                            MAX_LENGTH_NAME_ING, MAX_LENGTH_NAME_REC,
                            MAX_LENGTH_NAME_TAG, MAX_LENGTH_SLUG_TAG,
                            MIN_AMOUNT_INGREDIENT_INREC, MIN_COOKING_TIME_REC)
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_NAME_ING,
    )
    meashurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=MAX_LENGTH_MEASUREMENT_UNIT_ING,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'meashurement_unit'],
                name='unique_ingredient_name',
            )
        ]

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_NAME_TAG,
        unique=True,
        help_text='Максимальная длинна 200 символов',
    )
    color = models.CharField(
        max_length=MAX_LENGTH_COLOR_TAG,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message='Поле должно сотостоять из 7 символов, начиная с "#"',
            )
        ],
        help_text='Введите цвет в формате HEX (например, "#FF0000")',
    )
    slug = models.SlugField(
        verbose_name='Уникальный слаг',
        max_length=MAX_LENGTH_SLUG_TAG,
        unique=True,
        help_text='Максимальная длинна 200 символов',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список тегов',
        related_name='recipes',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь (В рецепте - автор рецепта)',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientOnRecipe',
        verbose_name='Список ингредиентов',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_NAME_REC,
    )
    image = models.ImageField(
        verbose_name='Ссылка на картинку на сайте',
        blank=True,
        null=True,
        upload_to='images/%Y/%m/%d',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[
            MinValueValidator(
                MIN_COOKING_TIME_REC,
                message='Значение должно быть больше '
            ),
            MaxValueValidator(
                MAX_COOKING_TIME_REC,
                message='Значение должно быть меньше'
            )
        ],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientOnRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_amount',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients_amount',
        verbose_name='Ингриденты',
    )
    amount = models.PositiveSmallIntegerField(
        default=DEFAULT_AMOUNT_INGREDIENT_INREC,
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                MIN_AMOUNT_INGREDIENT_INREC,
                message='Количество должно быть больше'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient',
            )
        ]

    def __str__(self):
        return f'{self.ingredient.name} - {self.amount}'


class BaseRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss'

    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(class)ss'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user} добавил {self.recipe.name}'


class FavoriteRecipe(BaseRecipe):
    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_favorite',
            )
        ]


class ShoppingList(BaseRecipe):
    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe',
            )
        ]
