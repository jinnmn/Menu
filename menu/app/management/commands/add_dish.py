from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Dish, Product, DishIngredient

class Command(BaseCommand):
    help = 'Добавляет блюдо в базу данных и пересчитывает ингредиенты на 1 кг'

    def handle(self, *args, **kwargs):
        # Создаем пользователя (если он еще не существует)
        user, created = User.objects.get_or_create(username='chef')

        # Продукты и их веса
        products = {
            'Яблоко': {'id': 1, 'brutto': 150, 'netto': 120},
            'Банан': {'id': 2, 'brutto': 120, 'netto': 110},
            'Апельсин': {'id': 3, 'brutto': 180, 'netto': 170},
            'Мёд': {'id': 20, 'brutto': 40, 'netto': 30},
            'Творог': {'id': 21, 'brutto': 100, 'netto': 95},
            'Орехи': {'id': 22, 'brutto': 30, 'netto': 25},
            'Йогурт': {'id': 23, 'brutto': 100, 'netto': 95},
        }

        # Получаем продукты из базы данных
        ingredient_objects = []
        total_brutto_weight = 0  # Общий вес брутто всех ингредиентов

        for name, data in products.items():
            try:
                product = Product.objects.get(id=data['id'])
                ingredient_objects.append({
                    'product': product,
                    'brutto': data['brutto'],
                    'netto': data['netto'],
                })
                total_brutto_weight += data['brutto']  # Суммируем общий вес брутто
            except Product.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Продукт {name} с ID {data['id']} не найден"))
                return

        # Если общий вес меньше или равен 0, не продолжаем
        if total_brutto_weight <= 0:
            self.stdout.write(self.style.ERROR("Общий вес ингредиентов равен или меньше 0, невозможно продолжить."))
            return

        # Рассчитываем коэффициент для пересчета на 1 кг (1000 г)
        scale_factor = 1000 / total_brutto_weight

        # Создаем блюдо
        dish = Dish.objects.create(
            name="Фрукты в йогурте с орехами (на 1 кг)",
            author=user,
            description="Фрукты с медом, творогом и йогуртом. Простое и вкусное блюдо.",
            dish_type="dessert",
            technology="Сложите все фрукты в миску, добавьте мед и творог, перемешайте.",
        )

        # Добавляем ингредиенты в блюдо через модель DishIngredient с пересчетом на 1 кг
        for ingredient in ingredient_objects:
            # Пересчитываем брутто и нетто для каждого ингредиента
            new_brutto = ingredient['brutto'] * scale_factor
            new_netto = ingredient['netto'] * scale_factor

            DishIngredient.objects.create(
                dish=dish,
                product=ingredient['product'],
                brutto=new_brutto,
                netto=new_netto
            )

        self.stdout.write(self.style.SUCCESS(f"Блюдо '{dish.name}' успешно добавлено с ингредиентами, пересчитанными на 1 кг!"))
