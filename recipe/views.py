from django.shortcuts import render, get_object_or_404
from .models import Recipe

def main(request):
    # Фільтруємо рецепти за 2023 рік
    recipes = Recipe.objects.filter(created_at__year=2023)
    return render(request, 'main.html', {'recipes': recipes})

def recipe_detail(request, id):
    # Отримуємо рецепт за його id або повертаємо 404 помилку
    recipe = get_object_or_404(Recipe, id=id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})