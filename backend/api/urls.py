from django.urls import include, path
from rest_framework import routers

from .views import (AdminIngredientViewSet, AdminTagViewSet, IngredientViewSet,
                    RecipeViewSet, TagViewSet, UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register(r'admin/tags', AdminTagViewSet, basename='admin-tags')
router.register(
    r'admin/ingredients', AdminIngredientViewSet, basename='admin-ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
