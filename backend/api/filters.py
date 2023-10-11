from django_filters.rest_framework import filters, FilterSet

from recipes.models import Recipe

class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    class Meta:
        model = Recipe
        fields = ['author', 'is_favorited']

    def get_is_favorited(self, queryset, name, value):
        current_user = self.request.user
        if value:
            return queryset.filter(favorites__user=current_user)
        return queryset