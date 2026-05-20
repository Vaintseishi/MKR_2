from django.shortcuts import render
from .models import Recipe

def main(request):
    # Фільтруємо рецепти, де рік створення дорівнює 2023
    recipes = Recipe.objects.filter(created_at__year=2023)
    return render(request, 'main.html', {'recipes': recipes})