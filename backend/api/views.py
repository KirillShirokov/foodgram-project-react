from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
# from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api import serializers
from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAdminOrAuthorOrReadOnly
from api.paginator import CustomPagination
from recipes.models import (FavoriteRecipe, Ingredient, IngredientOnRecipe,
                            Recipe, ShoppingList, Tag)
from users.models import Follow, User


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет ингридиентов"""
    permission_classes = (AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = None
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет тэгов"""
    permission_classes = (AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов"""
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    queryset = Recipe.objects.select_related('author').prefetch_related(
        'tags',
        'ingredients_amount',
        'ingredients_amount__ingredient'
    ).all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RecipeListSerializer
        return serializers.RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            raise PermissionDenied("Вы не можете обновлять этот рецепт!")
        kwargs["partial"] = False
        return self.update(request, *args, **kwargs)

    @action(detail=True,
            methods=['POST'],
            permission_classes=(IsAuthenticated,)
            )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        ShoppingList.objects.create(
            user=request.user,
            recipe=recipe
        )
        serializer = serializers.ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=201)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        get_object_or_404(ShoppingList,
                          recipe=pk,
                          user=request.user).delete()
        return Response(status=204)

    @action(detail=False,
            methods=['GET'],
            permission_classes=(IsAuthenticated,)
            )
    def download_shopping_cart(self, request):
        current_user = request.user
        ingredients = IngredientOnRecipe.objects.filter(
            recipe__shoppinglists__user=current_user
        ).values(
            'ingredient__name', 'ingredient__meashurement_unit'
        ).annotate(
            total_amount=Sum('amount')
        ).order_by('ingredient__name')

        shopping_list = 'Список покупок\n'
        for ingredient in ingredients:
            shopping_list += (
                f'{ingredient["ingredient__name"]}'
                f'({ingredient["ingredient__meashurement_unit"]}) - '
                f'{ingredient["total_amount"]}\n'
            )
        response = HttpResponse(shopping_list, 'Content-Type: text/plain')
        response[
            'Content-Dispoisition'
        ] = 'attachement; filename="shopping_list.txt"'
        return response

    @action(detail=True,
            methods=['POST'],
            permission_classes=(IsAuthenticated,)
            )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        FavoriteRecipe.objects.create(
            user=request.user,
            recipe=recipe
        )
        serializer = serializers.ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=201)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        get_object_or_404(FavoriteRecipe,
                          recipe=pk,
                          user=request.user).delete()
        return Response(status=204)


class UserViewSet(DjoserUserViewSet):
    """Вьюсет действий юзера"""

    @action(detail=False,
            methods=['GET'],
            permission_classes=(IsAuthenticated,)
            )
    def subscriptions(self, request):
        authors = User.objects.filter(
            following__user=request.user
        )
        page = self.paginate_queryset(authors)
        serializer = serializers.UserWithRecipesSerializer(
            page,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=['POST'],
            permission_classes=(IsAuthenticated,)
            )
    def subscribe(self, request, id):
        author = get_object_or_404(User, pk=id)
        Follow.objects.create(
            user=request.user,
            following=author
        )
        serializer = serializers.UserWithRecipesSerializer(
            author,
            context={'request': request}
        )
        return Response(serializer.data, status=201)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        get_object_or_404(Follow, user=request.user, following=id).delete()
        return Response(status=204)
