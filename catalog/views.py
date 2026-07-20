from django.shortcuts import render
from catalog.models import Product

def home(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, "home.html", context)


def contacts(request):
    return render(request, "contacts.html")

def product_detail(request, pr_id):
    product = Product.objects.get(id=pr_id)
    context = {
        'name': product.name,
        'description': product.description,
        'image': product.image,
        'category': product.category,
        'price': product.price,

    }
    return render(request, 'product_detail.html', context)
