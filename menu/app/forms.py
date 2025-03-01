from django import forms
from .models import Product, Dish, DishIngredient

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'calories', 'proteins', 'fats', 'carbohydrates']
        labels = {
            'name': 'Название продукта',
            'price': 'Цена (руб/кг)',
            'calories': 'Калорийность (ккал/100г)',
            'proteins': 'Белки (г/100г)',
            'fats': 'Жиры (г/100г)',
            'carbohydrates': 'Углеводы (г/100г)',
        }

    error_messages = {
        'name': {
            'required': 'Поле "Название продукта" обязательно для заполнения.',
        },
        'price': {
            'required': 'Поле "Цена" обязательно для заполнения.',
            'invalid': 'Введите корректную цену.',
        },
        'calories': {
            'required': 'Поле "Калорийность" обязательно для заполнения.',
        },
        'proteins': {
            'required': 'Поле "Белки" обязательно для заполнения.',
        },
        'fats': {
            'required': 'Поле "Жиры" обязательно для заполнения.',
        },
        'carbohydrates': {
            'required': 'Поле "Углеводы" обязательно для заполнения.',
        },
    }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            return name.strip().capitalize()  # Приводим первую букву к заглавной
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Цена должна быть больше 0.")
        return price

    def clean_calories(self):
        calories = self.cleaned_data.get('calories')
        if calories < 0:
            raise forms.ValidationError("Калорийность не может быть отрицательной.")
        return calories

    def clean_proteins(self):
        proteins = self.cleaned_data.get('proteins')
        if proteins < 0:
            raise forms.ValidationError("Белки не могут быть отрицательными.")
        return proteins

    def clean_fats(self):
        fats = self.cleaned_data.get('fats')
        if fats < 0:
            raise forms.ValidationError("Жиры не могут быть отрицательными.")
        return fats

    def clean_carbohydrates(self):
        carbohydrates = self.cleaned_data.get('carbohydrates')
        if carbohydrates < 0:
            raise forms.ValidationError("Углеводы не могут быть отрицательными.")
        return carbohydrates

class DishIngredientForm(forms.ModelForm):
    class Meta:
        model = DishIngredient
        fields = ['product', 'brutto', 'netto']

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'photo', 'dish_type', 'technology']

    # Поля для ингредиентов
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )