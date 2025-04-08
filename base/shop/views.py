from django.shortcuts import get_object_or_404, render
from .models import Category, Product

def all_products(request):
    products = Product.objects.all()
    return render(request, 'shop/all_products.html', {'products': products})

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'products': products
    })

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    return render(request, 'shop/product_detail.html', {'product': product})