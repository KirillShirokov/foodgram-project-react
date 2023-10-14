from django.urls import include, path

from rest_framework import routers

from api.views import (TagViewSet,
                       IngredientsViewSet,
                       RecipeViewSet,
                       UserViewSet)


router_v1 = routers.DefaultRouter()
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientsViewSet)
router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
