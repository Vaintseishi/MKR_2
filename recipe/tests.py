from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from recipe.models import Recipe, Category

class RecipeViewsTestCase(TestCase):
    def setUp(self):
        # Створюємо категорію
        self.category = Category.objects.create(name="Test Category")
        
        # Створюємо рецепт, який буде за 2023 рік
        self.recipe_2023 = Recipe.objects.create(
            title="Recipe 2023",
            description="Tasty",
            instructions="Cook it",
            ingredients="Salt",
            category=self.category
        )
        # Примусово оновлюємо дату на 2023 рік, обходячи auto_now_add
        Recipe.objects.filter(id=self.recipe_2023.id).update(created_at=timezone.datetime(2023, 6, 15, tzinfo=timezone.utc))
        self.recipe_2023.refresh_from_db()

        # Створюємо рецепт за поточний (2026) рік
        self.recipe_2026 = Recipe.objects.create(
            title="Recipe 2026",
            description="Fresh",
            instructions="Bake it",
            ingredients="Sugar",
            category=self.category
        )

    def test_main_view_status_code_and_context(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, що в контексті є рецепт за 2023 і немає за 2026
        self.assertIn(self.recipe_2023, response.context['recipes'])
        self.assertNotIn(self.recipe_2026, response.context['recipes'])

    def test_recipe_detail_view_success(self):
        response = self.client.get(reverse('recipe_detail', args=[self.recipe_2023.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['recipe'].title, "Recipe 2023")

    def test_recipe_detail_view_404(self):
        response = self.client.get(reverse('recipe_detail', args=[999])) # Неіснуючий ID
        self.assertEqual(response.status_code, 404)