import random

from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product


# Create your views here.

def get_menu():
    return ProductCategory.objects.all()

def get_hot_product():
    # products = Product.objects.all()
    products_id = Product.objects.values_list('id', flat=True)
    hot_product_id = random.choice(products_id)
    return Product.objects.get(pk=hot_product_id)


def related_products(product):
    return Product.objects.filter(category=product.category).exclude(id=product.id)



def index(request):
    context = { 'page_title': 'Интернет магазин СмартПеченька',}
    return render(request, "mainapp/index.html", context=context)



def catalog(request):
    categories = ProductCategory.objects.all()

    hot_product = get_hot_product()
    _related_products = related_products(hot_product)

    context = { 'page_title': 'Каталог',
                'categories': get_menu(),
                'hot_product': hot_product,
                'related_products': _related_products,
                }
    return render(request, "mainapp/catalog.html", context=context)

def catalog_products(request, pk):
    if int(pk) == 0:
        category = {'pk': 0, 'name': 'Все'}
        products = Product.objects.all()
        # products = request.user.product_set.all()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = Product.objects.filter(category=category)

    context = {'page_title': 'Каталог',
               'category': category,
               'categories': get_menu(),
               'products': products,

               }
    return render(request, "mainapp/catalog_products.html", context=context)


def product_page(request, pk):
    context = {
        'page_title': 'продукт',
        'categories': get_menu(),
        'product': get_object_or_404(Product, pk=pk),
    }
    return render(request, 'mainapp/product_page.html', context)


def contacts(request):
    locations = [

        {
            'phone': 'xxxxxxxxx',
            'street': 'Пиченкина 11',
            'email': 'smartpicenki@gmail.com',
        }
    ]

    context = { 'page_title': 'Контакты',
                'locations': locations,
    
    }
    return render(request, "mainapp/contacts.html", context=context)