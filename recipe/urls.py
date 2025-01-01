from django.urls import path
from .views import (
    RecipeListView, UserRecipeListView, RecipeDetailView,
    RecipeCreateView, RecipeUpdateView, RecipeDeleteView,
    IngredientCreateView, IngredientUpdateView, IngredientDeleteView,InstructionCreateView,InstructionUpdateView,InstructionDeleteView
)


app_name = 'recipe'

urlpatterns = [
    path('', RecipeListView.as_view(), name='view_recipes'),
    path('me/', UserRecipeListView.as_view(), name='view_user_recipes'),
    path('recipe/<int:pk>/', RecipeDetailView.as_view(), name='view_recipe_detail'),
    path('create/', RecipeCreateView.as_view(), name='create_recipe'),
    path('update/<int:pk>/', RecipeUpdateView.as_view(), name='update_recipe'),
    path('recipe/delete/<int:pk>/', RecipeDeleteView.as_view(), name='delete_recipe'),
    path('<int:recipe_primary_key>/ingredient/create/', IngredientCreateView.as_view(), name='create_ingredient'),
    path('<int:recipe_primary_key>/ingredient/update/<int:pk>/', IngredientUpdateView.as_view(), name='update_ingredient'),
    path('<int:recipe_primary_key>/ingredient/delete/<int:pk>/', IngredientDeleteView.as_view(), name='delete_ingredient'),
    path('<int:recipe_primary_key>/instruction/create/', InstructionCreateView.as_view(), name='create_instruction'),
    path('<int:recipe_primary_key>/instruction/update/<int:instruction_primary_key>/', InstructionUpdateView.as_view(), name='update_instruction'),
    path('<int:recipe_primary_key>/instruction/delete/<int:instruction_primary_key>/', InstructionDeleteView.as_view(), name='delete_instruction'),
]