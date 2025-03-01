from django.contrib import admin
from .models import Dish, DishIngredient, Product
from django.utils.safestring import mark_safe

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'dish_type', 'description', 'technology', 'display_ingredients','display_photo')

    fieldsets = (
        (None, {
            'fields': ('name', 'author', 'description', 'technology', 'dish_type', 'photo')  # Добавляем поле photo
        }),
    )

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

    def display_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" />')
        return "Нет фото"

    display_photo.short_description = "Фото"

    display_ingredients.allow_tags = True  # Разрешаем отображение HTML в таблице

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'calories', 'proteins', 'fats', 'carbohydrates')
    search_fields = ('name',)
    list_filter = ('price',)
    ordering = ('name',)
