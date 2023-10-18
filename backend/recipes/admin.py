from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, IngredientOnRecipe, Recipe,
                     ShoppingList, Tag)


class RecipeIngredientsInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 0
    min_num = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'meashurement_unit',
    )
    list_display_links = (
        'name',
    )
    search_fields = ('name',)
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    list_display_links = (
        'name',
    )
    search_fields = ('name',)
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        'pub_date',
    )
    list_display_links = (
        'name',
    )
    inlines = (RecipeIngredientsInline, )
    search_fields = ('name',)
    list_filter = ('pub_date',)


class IngredientOnRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'ingredient',
        'amount'
    )
    list_display_links = (
        'recipe',
    )


class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_display_links = (
        'user',
    )
    search_fields = ('user',)
    list_filter = ('user',)


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    list_display_links = (
        'user',
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientOnRecipe, IngredientOnRecipeAdmin)
admin.site.register(FavoriteRecipe, FavoriteRecipeAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
