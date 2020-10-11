# from mainapp.models import ProductCategory
#
#
# def mainmenu(requests):
#     return {
#     'mainmenu': ProductCategory.objects.all(),
#         # 'mainmenu': ProductCategory.Product.filter(is_active=True),
#     }

from django.core.cache import cache

from geekshop import settings
from mainapp.models import ProductCategory


def mainmenu(request):
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
    else:
        links_menu = ProductCategory.objects.filter(is_active=True)

    return {
        'mainmenu': links_menu
    }
