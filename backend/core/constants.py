"""Константы модели ингредиента (Ingredient)"""
MAX_LENGTH_NAME_ING = 200
MAX_LENGTH_MEASUREMENT_UNIT_ING = 200

"""Константы модели тега (Tag)"""
MAX_LENGTH_NAME_TAG = 200
MAX_LENGTH_COLOR_TAG = 7
MAX_LENGTH_SLUG_TAG = 200

"""Констанаты модели рецепта (Recipe)"""
MAX_LENGTH_NAME_REC = 200
MIN_COOKING_TIME_REC = 1
MAX_COOKING_TIME_REC = 1440

"""Константы модели ингредиента в рецепте (Ingredient On Recipe)"""
MIN_AMOUNT_INGREDIENT_INREC = 1
DEFAULT_AMOUNT_INGREDIENT_INREC = 1

"""Константы модели пользователя (User)"""
MAX_LENGTH_EMAIL_USER = 250
MAX_LENGTH_USERNAME_USER = 150
MAX_LENGTH_FIRST_NAME_USER = 150
MAX_LENGTH_LAST_NAME_USER = 150

"""Константы для DRF"""
PAGINATION_PAGE_SIZE = 6