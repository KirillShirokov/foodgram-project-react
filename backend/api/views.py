from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import filters, mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from api.filters import RecipeFilter
from api import serializers
from api.permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from recipes.models import *
from users.models import Follow


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет ингридиентов'''
    permission_classes = (AllowAny,)
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет тэгов'''
    permission_classes = (AllowAny,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    '''Вьюсет рецептов'''
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter


    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.RecipeListSerializer
        return serializers.RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True,methods=['POST', 'DELETE'], permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            ShoppingList.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = serializers.ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=201)
        ShoppingList.objects.filter(recipe=recipe, user=request.user).delete()
        return Response(status=204)
    
    @action(detail=True,methods=['GET'], permission_classes=(IsAuthenticated,))
    def is_in_shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = serializers.ShortRecipeSerializer(recipe)
        return Response(serializer.data, status=201)
        
    
    @action(detail=True,methods=['POST', 'DELETE'], permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            FavoriteRecipe.objects.create(
                user=request.user,
                recipe=recipe
            )
            serializer = serializers.ShortRecipeSerializer(recipe)
            return Response(serializer.data, status=201)
        FavoriteRecipe.objects.filter(recipe=recipe, user=request.user).delete()
        return Response(status=204)


class UserViewSet(DjoserUserViewSet):
    '''Вьюсет действий юзера'''

    @action(detail=False, methods=['GET'], permission_classes=(IsAuthenticated,))
    def subscriptions(self, request):
        authors = User.objects.filter(
            following__user=request.user
        )
        page = self.paginate_queryset(authors)
        serializer = serializers.UserWithRecipesSerializer(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)
    
    @action(detail=True, methods=['POST', 'DELETE'], permission_classes=(IsAuthenticated,))
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            Follow.objects.create(
                user=request.user,
                following=author
            )
            serializer = serializers.UserWithRecipesSerializer(author, context={'request': request})
            return Response(serializer.data, status=201)
        
        Follow.objects.filter(user=request.user, following=author).delete()
        return Response(status=204)
        

        

        