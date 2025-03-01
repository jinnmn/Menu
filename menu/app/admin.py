from django.contrib import admin
from .models import Dish
from django.utils.safestring import mark_safe

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'dish_type', 'description', 'technology', 'display_ingredients')

    def display_ingredients(self, obj):
        # Преобразуем ингредиенты блюда в HTML таблицу
        html = "<table border='1' style='width: 100%; border-collapse: collapse;'>"
        html += "<tr><th>Ингредиент</th><th>Брутто (г)</th><th>Нетто (г)</th></tr>"

        # Получаем все ингредиенты для текущего блюда
        for dish_ingredient in obj.ingredients.all():
            ingredient_name = dish_ingredient.product.name
            brutto = dish_ingredient.brutto
            netto = dish_ingredient.netto
            html += f"<tr><td>{ingredient_name}</td><td>{brutto:.2f}</td><td>{netto:.2f}</td></tr>"

        html += "</table>"
        return mark_safe(html)

    display_ingredients.allow_tags = True  # Разрешаем отображение HTML в таблице
