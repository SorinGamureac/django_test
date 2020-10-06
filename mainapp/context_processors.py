from mainapp.models import ProductCategory


def mainmenu(requests):
    return {
    'mainmenu': ProductCategory.objects.all(),
        # 'mainmenu': ProductCategory.Product.filter(is_active=True),
    }