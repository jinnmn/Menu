from django.shortcuts import render
from .models import Product
# Create your views here.
def add_product(request):
    return render(request, 'app/add_product.html')

def add_recipe(request):
    return render(request, 'app/add_recipe.html')

def product_list(request):
    query = request.GET.get('search', '')
    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'app/products.html', {'products': products, 'search_query': query})