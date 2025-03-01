import random
import string

from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    calories = models.IntegerField()
    proteins = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class DishType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    DISH_TYPES = [
        ('cold_appetizer', 'Холодная закуска'),
        ('hot_appetizer', 'Горячая закуска'),
        ('salad', 'Салат'),
        ('first_course', 'Первое блюдо'),
        ('main_course', 'Основное блюдо'),
        ('dessert', 'Десерт'),
        ('drink', 'Напиток'),
    ]

    name = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='dish_photos/', null=True, blank=True)
    dish_type = models.CharField(max_length=20, choices=DISH_TYPES)
    technology = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.photo:
            # назвать по айдишникам не получилось(ибо их пока нет(()
            random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
            extension = self.photo.name.split('.')[-1]  # Получаем расширение файла
            new_filename = f"{random_filename}.{extension}"
            self.photo.name = new_filename

        super().save(*args, **kwargs)


    def clean(self):
        if not self.name:
            raise ValidationError('Название блюда не может быть пустым.')

        if len(self.name) > 255:
            raise ValidationError('Название блюда не может превышать 255 символов.')

        if not self.description:
            raise ValidationError('Описание блюда не может быть пустым.')

        if self.photo:
            file_extension = self.photo.name.split('.')[-1].lower()
            if file_extension not in ['jpg', 'jpeg', 'png']:
                raise ValidationError('Поддерживаются только изображения в формате jpg, jpeg и png.')

        if self.dish_type not in dict(DISH_TYPES):
            raise ValidationError('Неверный тип блюда.')

    def clean_fields(self, exclude=None):
        self.clean()
        super().clean_fields(exclude=exclude)


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, related_name='ingredients', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brutto = models.DecimalField(max_digits=10, decimal_places=2)
    netto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.brutto}g (брутто), {self.netto}g (нетто)"

    def clean(self):

        if not self.product:
            raise ValidationError(f'Продукт {self.product} не существует в базе данных.')

        if self.brutto <= 0:
            raise ValidationError(f'Брутто для {self.product.name} должно быть больше 0.')
        if self.netto <= 0:
            raise ValidationError(f'Нетто для {self.product.name} должно быть больше 0.')

    def clean_fields(self, exclude=None):
        self.clean()
        super().clean_fields(exclude=exclude)
