import base64
from django.db.transaction import atomic
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.core.files.base import ContentFile

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import (
    Ingredient,
    Tag,
    Recipe,
    IngredientOnRecipe,
)
from users.models import User


class Base64ImageField(serializers.ImageField):
    """Обработка изображения"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор кастомного юзера"""
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class CustomUserSerializer(UserSerializer):
    """Сериализатор расштренного кастомного юзера, с отображением подписки"""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.following.filter(user=user).exists()


class UserWithRecipesSerializer(CustomUserSerializer):
    """Сериализтор кастомного юзера с рецептом и счетчиком"""
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, user):
        recipes_limit = self.context['request'].GET.get(
            'recipes_limit', default=3
        )
        recipes_user = user.recipes.all()[:int(recipes_limit)]
        return ShortRecipeSerializer(recipes_user, many=True).data

    def get_recipes_count(self, user):
        return user.recipes.count()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента"""
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента в рецепте"""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.meashurement_unit'
    )

    class Meta:
        model = IngredientOnRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор количества ингредиента в создании рецепта"""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientOnRecipe
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""
    class Meta:
        model = Tag
        fields = ('__all__')


class AddTagSerializer(serializers.ModelSerializer):
    """Сериализатор добавления тегов"""
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Tag
        fields = ('__all__')


class RecipeListSerializer(serializers.ModelSerializer):
    """Сериализатор отображения списка рецептов"""
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer()
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredients_amount'
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, recipe):
        user = self.context['request'].user
        return not user.is_anonymous and (recipe.
                                          favoriterecipes.
                                          filter(user=user).exists())

    def get_is_in_shopping_cart(self, recipe):
        user = self.context['request'].user
        return not user.is_anonymous and (recipe.
                                          shoppinglists.
                                          filter(user=user).exists())


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания рецепта"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
    )
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = AddIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    @atomic
    def create(self, validate_data):
        tags = validate_data.pop('tags')
        ingredients = validate_data.pop('ingredients')
        recipe = Recipe.objects.create(**validate_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, recipe, validate_data):
        tags = validate_data.pop('tags')
        ingredients = validate_data.pop('ingredients')
        recipe = super().update(recipe, validate_data)
        recipe.tags.set(tags)
        recipe.ingredients_amount.all().delete()
        self.create_ingredients(ingredients, recipe)
        return recipe

    @staticmethod
    def create_ingredients(ingredients, recipe):
        ingredients = [
            IngredientOnRecipe(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        IngredientOnRecipe.objects.bulk_create(ingredients)

    def to_representation(self, recipe):
        return RecipeListSerializer(recipe, context=self.context).data


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта(укороченная версия)"""
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = ('id',
                  'name',
                  'image',
                  'cooking_time')
