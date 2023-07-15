from shop.models import Category

def menu_link(request):
    links=Category.objects.all()
    return{'links':links}
