from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime
from recipe.models import Recipe, Category

class RecipeViewsTestCase(TestCase):
    def setUp(self):
        # 1. Створюємо тестову категорію
        self.category = Category.objects.create(name="Тестова категорія")
        
        # 2. Створюємо рецепт за 2023 рік
        self.recipe_2023 = Recipe.objects.create(
            title="Рецепт 2023 року",
            description="Дуже смачна страва",
            instructions="Змішати і запекти",
            ingredients="Борошно, цукор, яйця",
            category=self.category
        )
        # Примусово оновлюємо дату створення на 2023 рік
        Recipe.objects.filter(id=self.recipe_2023.id).update(
            created_at=datetime.datetime(2023, 8, 24, tzinfo=datetime.UTC)
        )
        self.recipe_2023.refresh_from_db()

        # 3. Створюємо рецепт за поточний рік (щоб перевірити фільтрацію)
        self.recipe_current = Recipe.objects.create(
            title="Сучасний рецепт",
            description="Нова страва",
            instructions="Посмажити",
            ingredients="М'ясо, спеції",
            category=self.category
        )

    def test_main_view_status_code_and_context(self):
        """Перевірка, що main view повертає 200 та містить ТІЛЬКИ рецепти за 2023 рік"""
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        
        # Перевіряємо наявність правильної змінної в контексті шаблону
        self.assertIn('recipes', response.context)
        
        # Перевіряємо, що рецепт 2023 року відображається, а поточного року — ні
        self.assertIn(self.recipe_2023, response.context['recipes'])
        self.assertNotIn(self.recipe_current, response.context['recipes'])
        
        # Перевіряємо, що дані виводяться на сторінку HTML
        self.assertContains(response, "Рецепт 2023 року")
        self.assertNotContains(response, "Сучасний рецепт")

    def test_main_view_empty_list(self):
        """Перевірка відображення тексту, якщо рецептів за 2023 рік немає (тест блоку {% empty %})"""
        # Видаляємо єдиний рецепт за 2023 рік
        self.recipe_2023.delete()
        
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        # Шаблон main.html має вивести повідомлення з блоку {% empty %}
        self.assertContains(response, "No recipes found.")

    def test_recipe_detail_view_success(self):
        """Перевірка успішного відображення деталей існуючого рецепту"""
        response = self.client.get(reverse('recipe_detail', args=[self.recipe_2023.id]))
        self.assertEqual(response.status_code, 200)
        
        # Перевіряємо об'єкт у контексті
        self.assertEqual(response.context['recipe'], self.recipe_2023)
        
        # Перевіряємо, чи рендеряться тексти з полів моделі на сторінці
        self.assertContains(response, "Рецепт 2023 року")
        self.assertContains(response, "Дуже смачна страва")
        self.assertContains(response, "Борошно, цукор, яйця")

    def test_recipe_detail_view_404(self):
        """Перевірка, що запит неіснуючого рецепту повертає статус 404 (Not Found)"""
        invalid_id = 99999
        response = self.client.get(reverse('recipe_detail', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)