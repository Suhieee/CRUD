from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .models import Category, Recipe, Ingredient, Instruction
from .forms import RecipeForm, IngredientForm, InstructionForm


class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipe/view_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        query = self.request.GET.get('query', '').strip()
        category_id = self.request.GET.get('category', '').strip()

        recipes = Recipe.objects.all()

        # Filter by category if category is specified
        if category_id.isdigit() and int(category_id) > 0:
            recipes = recipes.filter(category_id=int(category_id))

        # Filter by search query if provided
        if query:
            recipes = recipes.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Add categories to context
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class UserRecipeListView(ListView):
    model = Recipe
    template_name = 'recipe/view_user_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(created_by=self.request.user)


class RecipeDetailView(LoginRequiredMixin,DetailView):
    model = Recipe
    template_name = 'recipe/view_recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context['ingredients'] = Ingredient.objects.filter(recipe=recipe)
        context['instructions'] = Instruction.objects.filter(recipe=recipe)
        return context


class RecipeCreateView(LoginRequiredMixin,CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe/form.html'
    success_url = reverse_lazy('recipe:view_recipes')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Recipe created successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Recipe creation failed. Please correct the errors and try again.')
        return super().form_invalid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe/form.html'
    context_object_name = 'recipe'
    success_url = reverse_lazy('recipe:view_recipes')  

    def get_queryset(self):
        return Recipe.objects.filter(created_by=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Dish Updated Successfully')
        return super().form_valid(form)

class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'recipe/confirm_delete.html' 
    context_object_name = 'recipe'
    success_url = reverse_lazy('recipe:view_recipes')  # Redirect to the recipe list after deletion

    def test_func(self):
        # Ensure the user is the creator of the recipe
        recipe = self.get_object()
        return self.request.user == recipe.created_by

    def delete(self, request, *args, **kwargs):
        recipe = self.get_object()  # Get the recipe object before deletion
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'Recipe "{recipe.title}" deleted successfully!') 
        return response 

    def get_success_url(self):
        # Redirect to the list of recipes since the recipe is deleted
        return reverse_lazy('recipe:view_recipes')


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'recipe/form.html'

    def form_valid(self, form):
        # Set the recipe for the ingredient based on the URL parameter
        form.instance.recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_primary_key'])
        messages.success(self.request, 'Ingredient created successfully')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the recipe detail page
        return reverse_lazy('recipe:view_recipe_detail', kwargs={'pk': self.kwargs['recipe_primary_key']})
    

class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'recipe/form.html'
    context_object_name = 'ingredient'

    def get_queryset(self):
        # Ensure only the ingredients of the current user are visible
        return Ingredient.objects.filter(recipe__created_by=self.request.user)

    def form_valid(self, form):
        # Add a success message after the form is successfully updated
        messages.success(self.request, 'Ingredient updated successfully')
        return super().form_valid(form)

    def get_success_url(self):
     return reverse_lazy('recipe:view_recipe_detail', kwargs={'pk': self.kwargs['recipe_primary_key']})


class IngredientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ingredient
    template_name = 'recipe/confirm_delete.html'
    context_object_name = 'ingredient'

    def test_func(self):
        # Ensure the user is the creator of the recipe associated with the ingredient
        ingredient = self.get_object()  
        return self.request.user == ingredient.recipe.created_by  

    def get_success_url(self):
        # Add a success message and redirect to the recipe detail page
        messages.success(self.request, 'Ingredient deleted successfully!')
        return reverse_lazy('recipe:view_recipe_detail', kwargs={'pk': self.kwargs['recipe_primary_key']})


def delete(self, request, *args, **kwargs):
        # Optionally add a success message before deletion
           messages.success(self.request, 'Ingredients created successfully')
           return super().delete(request, *args, **kwargs)
    
class InstructionCreateView(LoginRequiredMixin, CreateView):
    model = Instruction
    form_class = InstructionForm
    template_name = 'recipe/form.html'

    def form_valid(self, form):
        # Associate the instruction with the recipe
        form.instance.recipe = get_object_or_404(Recipe, pk=self.kwargs['recipe_primary_key'])
        messages.success(self.request, 'Instruction created successfully')
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the recipe detail page
        return reverse_lazy('recipe:view_recipe_detail', kwargs={'pk': self.kwargs['recipe_primary_key']})
    
class InstructionUpdateView(LoginRequiredMixin, UpdateView):
    model = Instruction
    form_class = InstructionForm
    template_name = 'recipe/form.html'
    context_object_name = 'instruction'

    def get_queryset(self):
        return Instruction.objects.filter(recipe__created_by=self.request.user)

    def get_object(self, queryset=None):
        return Instruction.objects.get(pk=self.kwargs['instruction_primary_key'])

    def form_valid(self, form):
        # Add a success message after the form is successfully updated
        messages.success(self.request, 'Instruction updated successfully')
        return super().form_valid(form)

    def get_success_url(self):
     return reverse_lazy('recipe:view_recipe_detail', kwargs={'pk': self.kwargs['recipe_primary_key']})
    
class InstructionDeleteView(LoginRequiredMixin, DeleteView):
    model = Instruction
    template_name = 'recipe/confirm_delete.html'
    context_object_name = 'instruction'

    def get_object(self, queryset=None):
        # Use the instruction_primary_key from kwargs to get the Instruction object
        return get_object_or_404(Instruction, pk=self.kwargs['instruction_primary_key'])

    def test_func(self):
        # Ensure the user is the creator of the recipe
        instruction = self.get_object()
        return self.request.user == instruction.recipe.created_by

    def get_success_url(self):
        messages.success(self.request, 'Instruction deleted successfully')
        return reverse_lazy('recipe:view_recipe_detail', kwargs={'pk': self.kwargs['recipe_primary_key']})
    


class IngredientDeleteView(LoginRequiredMixin,DeleteView):
    model = Ingredient
    template_name = 'recipe/confirm_delete.html'
    context_object_name = 'ingredient'
    

    def test_func(self):
        # Ensure the user is the creator of the recipe
        recipe = self.get_object()
        return self.request.user == recipe.created_by
    
    def get_success_url(self):
        messages.success(self.request, 'Ingredients deleted successfully')
        return reverse_lazy('recipe:view_recipe_detail', kwargs={'pk': self.kwargs['recipe_primary_key']})
