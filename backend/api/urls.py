from django.urls import include, path

from djoser.views import UserViewSet
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import *


router_v1 = routers.DefaultRouter()
router_v1.register(r'tags', TagViewSet)
router_v1.register(r'ingredients', IngredientsViewSet)
router_v1.register(r'recipes', RecipeViewSet)
router_v1.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    # path('', include('djoser.urls')),
    # path('', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
]
 