from django.core.management.base import BaseCommand
from app.models import Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Заполнение базы данных продуктами для тестирования'

    def handle(self, *args, **kwargs):
        # Данные продуктов для заполнения
        products = [
            {'name': 'Яблоко', 'price': '70.00', 'calories': 52, 'proteins': '0.3', 'fats': '0.2',
             'carbohydrates': '14.0'},
            {'name': 'Банан', 'price': '60.00', 'calories': 89, 'proteins': '1.1', 'fats': '0.3',
             'carbohydrates': '23.0'},
            {'name': 'Апельсин', 'price': '90.00', 'calories': 47, 'proteins': '0.9', 'fats': '0.1',
             'carbohydrates': '12.0'},
            {'name': 'Киви', 'price': '120.00', 'calories': 41, 'proteins': '0.8', 'fats': '0.4',
             'carbohydrates': '10.0'},
            {'name': 'Груша', 'price': '85.00', 'calories': 57, 'proteins': '0.4', 'fats': '0.1',
             'carbohydrates': '15.0'},
            {'name': 'Помидор', 'price': '40.00', 'calories': 18, 'proteins': '0.9', 'fats': '0.2',
             'carbohydrates': '3.9'},
            {'name': 'Огурец', 'price': '35.00', 'calories': 15, 'proteins': '0.7', 'fats': '0.1',
             'carbohydrates': '3.6'},
            {'name': 'Картофель', 'price': '50.00', 'calories': 77, 'proteins': '2.0', 'fats': '0.1',
             'carbohydrates': '17.5'},
            {'name': 'Морковь', 'price': '45.00', 'calories': 41, 'proteins': '0.9', 'fats': '0.2',
             'carbohydrates': '9.6'},
            {'name': 'Капуста', 'price': '30.00', 'calories': 25, 'proteins': '1.3', 'fats': '0.1',
             'carbohydrates': '5.8'},
            {'name': 'Куриный бульон', 'price': '120.00', 'calories': 40, 'proteins': '6.0', 'fats': '1.0',
             'carbohydrates': '2.0'},
            {'name': 'Курица (грудка)', 'price': '350.00', 'calories': 165, 'proteins': '31.0', 'fats': '3.6',
             'carbohydrates': '0.0'},
            {'name': 'Говядина (постная)', 'price': '400.00', 'calories': 250, 'proteins': '26.0', 'fats': '17.0',
             'carbohydrates': '0.0'},
            {'name': 'Свинина (постная)', 'price': '380.00', 'calories': 242, 'proteins': '22.0', 'fats': '16.0',
             'carbohydrates': '0.0'},
            {'name': 'Шпинат', 'price': '60.00', 'calories': 23, 'proteins': '2.9', 'fats': '0.4',
             'carbohydrates': '3.6'},
            {'name': 'Перец болгарский', 'price': '50.00', 'calories': 20, 'proteins': '0.9', 'fats': '0.2',
             'carbohydrates': '4.7'},
            {'name': 'Чеснок', 'price': '30.00', 'calories': 149, 'proteins': '6.4', 'fats': '0.5',
             'carbohydrates': '33.1'},
            {'name': 'Лук', 'price': '40.00', 'calories': 40, 'proteins': '1.1', 'fats': '0.1', 'carbohydrates': '9.3'},
            {'name': 'Тыква', 'price': '60.00', 'calories': 26, 'proteins': '1.0', 'fats': '0.1',
             'carbohydrates': '6.5'},
            {'name': 'Куриные яйца', 'price': '80.00', 'calories': 143, 'proteins': '12.6', 'fats': '9.5',
             'carbohydrates': '1.1'},
            {'name': 'Молоко', 'price': '60.00', 'calories': 42, 'proteins': '3.4', 'fats': '1.0',
             'carbohydrates': '5.0'},
            {'name': 'Сыр', 'price': '250.00', 'calories': 402, 'proteins': '25.0', 'fats': '33.0',
             'carbohydrates': '1.3'},
            {'name': 'Творог', 'price': '150.00', 'calories': 98, 'proteins': '11.0', 'fats': '4.0',
             'carbohydrates': '3.0'},
            {'name': 'Рис', 'price': '70.00', 'calories': 130, 'proteins': '2.4', 'fats': '0.3',
             'carbohydrates': '28.0'},
            {'name': 'Макароны', 'price': '80.00', 'calories': 131, 'proteins': '5.0', 'fats': '1.1',
             'carbohydrates': '25.0'},
            {'name': 'Овсянка', 'price': '45.00', 'calories': 68, 'proteins': '2.5', 'fats': '1.4',
             'carbohydrates': '12.0'},
            {'name': 'Масло подсолнечное', 'price': '150.00', 'calories': 884, 'proteins': '0.0', 'fats': '100.0',
             'carbohydrates': '0.0'},
            {'name': 'Мёд', 'price': '200.00', 'calories': 304, 'proteins': '0.3', 'fats': '0.0',
             'carbohydrates': '82.4'},
            {'name': 'Шоколад', 'price': '300.00', 'calories': 546, 'proteins': '4.9', 'fats': '31.0',
             'carbohydrates': '61.0'}

        ]

        for product in products:
            product_obj, created = Product.objects.get_or_create(
                name=product['name'],
                defaults={
                    'price': Decimal(product['price']),
                    'calories': product['calories'],
                    'proteins': Decimal(product['proteins']),
                    'fats': Decimal(product['fats']),
                    'carbohydrates': Decimal(product['carbohydrates'])
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Продукт "{product["name"]}" добавлен в базу данных.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Продукт "{product["name"]}" уже существует.'))
