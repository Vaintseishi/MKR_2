from django.shortcuts import render
from .models import Recipe

def main(request):
    # Фільтруємо рецепти, де рік створення дорівнює 2023
    recipes = Recipe.objects.filter(created_at__year=2023)
    return render(request, 'main.html', {'recipes': recipes})

def recipe_detail(request, id):
    # Отримуємо рецепт за id або повертаємо 404
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})