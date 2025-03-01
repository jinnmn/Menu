from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Заполнение базы данных блюдами'

    def handle(self, *args, **kwargs):
        # Список продуктов
        Dish = apps.get_model('app', 'Dish')
        DishIngredient = apps.get_model('app', 'DishIngredient')
        Product = apps.get_model('app', 'Product')

        products_data = [
            {'name': 'Свекла', 'brutto': 200.00, 'netto': 150.00},
            {'name': 'Капуста свежая', 'brutto': 90.00, 'netto': 80.00},
            {'name': 'Лук репчатый', 'brutto': 60.00, 'netto': 40.00},
            {'name': 'Морковь', 'brutto': 80.00, 'netto': 60.00},
            {'name': 'Говядина отв. п/ф', 'brutto': 150.00, 'netto': 150.00},
            {'name': 'Ветчина в/к', 'brutto': 70.00, 'netto': 70.00},
            {'name': 'Сосиски', 'brutto': 70.00, 'netto': 70.00},
            {'name': 'Петрушка, корень', 'brutto': 40.00, 'netto': 30.00},
            {'name': 'Томат-пюре', 'brutto': 30.00, 'netto': 30.00},
            {'name': 'Сметана', 'brutto': 50.00, 'netto': 50.00},
            {'name': 'Бульон гов. из костей п/ф', 'brutto': 600.00, 'netto': 600.00},
            {'name': 'Соль', 'brutto': 4.00, 'netto': 4.00},
            {'name': 'Перец', 'brutto': 3.00, 'netto': 3.00},
            {'name': 'Лавровый лист', 'brutto': 2.00, 'netto': 2.00},
            {'name': 'Уксус 8%', 'brutto': 5.00, 'netto': 5.00}
        ]

        # Данные для блюда
        type_d = ('first_course', 'Первое блюдо')
        dish_name = 'Борщ'
        description = 'Традиционный борщ с овощами и мясом'
        technology = """1.Овощи нарезать соломкой. Свеклу отдельно тушить с жиром, томатом-пюре, сахаром. Спассерованные коренья и лук присоединить к свекле перед окончанием ее тушения.
        2. В процеженный бульон заложить капусту, куски мяса и мясных изделий, после закипания добавить свеклу и варить борщ 25—30 минут. За 10—15 минут до окончания варки положить лавровый лист, перец, соль.
        3.Доведенный до вкуса борщ должен быть кислосладким, наваристым (экстрактивным), с приятным свекольно-овощным запахом, в меру посоленным. Отдельно к борщу подать сметану и зелень.
        Выход: 1000 мл."""
        user = User.objects.get(id=3)  # Получаем пользователя по ID

        # Создаем и сохраняем блюдо
        new_dish = Dish(
            author=user,
            name=dish_name,
            description=description,
            dish_type=type_d,
            technology=technology
        )
        new_dish.save()  # Сохраняем блюдо в базе данных

        # Функция для создания списка ингредиентов
        def create_product_list(data, dish):
            ingredients = []
            for prod in data:
                # Создание объекта DishIngredient и связывание его с Dish
                ingredient = DishIngredient(
                    product=Product.objects.get(name=prod['name']),
                    brutto=prod['brutto'],
                    netto=prod['netto'],
                    dish=dish  # Присваиваем блюду
                )
                ingredient.save()  # Сохраняем ингредиент в базе
                ingredients.append(ingredient)  # Добавляем в список
            return ingredients

        # Создаем список ингредиентов и привязываем их к блюду
        ingredients = create_product_list(products_data, new_dish)

        # Выводим сообщение об успешном добавлении блюда
        self.stdout.write(self.style.SUCCESS(f'Блюдо "{dish_name}" успешно создано и добавлены ингредиенты.'))
