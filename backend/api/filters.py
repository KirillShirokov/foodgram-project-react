from django_filters.rest_framework import filters, FilterSet

from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['author', 'is_favorited', 'tags']

    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favoriterecipes__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shoppinglists__user=self.request.user)
        return queryset


class IngredientFilter(SearchFilter):
    search_param = 'name'
