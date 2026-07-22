from django.shortcuts import render, redirect,  get_object_or_404
from .forms import ProductForm
from catalog.models import Product


def home(request):
    products = Product.objects.all()
    context = {
        "products": products,
    }
    return render(request, "home.html", context)


def contacts(request):
    return render(request, "contacts.html")


def products_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        "name": product.name,
        "description": product.description,
        "image": product.image,
        "category": product.category,
        "price": product.price,

    }
    return render(request, "product_detail.html", context)

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # request.FILES обязателен для файлов!
        if form.is_valid():
            form.save()
            return redirect('product_list')  # или на страницу товара, если есть имя URL
    else:
        form = ProductForm()

    context = {'form': form}
    return render(request, 'product_create.html', context)
