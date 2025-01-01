from django.contrib import admin
from django.contrib import admin
from .models import Category, Recipe, Instruction, Ingredient

# Customizing Category admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Customizing Recipe admin
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_by', 'created_at', 'updated_at')
    list_filter = ('category', 'created_by')
    search_fields = ('name',)
    ordering = ('created_at',)

# Customizing Instruction admin
class InstructionAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'instruction_text', 'recipe')
    list_filter = ('recipe',)
    search_fields = ('instruction_text',)
    ordering = ('step_number',)

# Customizing Ingredient admin
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'metric', 'recipe')
    list_filter = ('recipe',)
    search_fields = ('name', 'quantity')
    ordering = ('recipe',)

# Registering the models with custom admin classes
admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Instruction, InstructionAdmin)
admin.site.register(Ingredient, IngredientAdmin)
