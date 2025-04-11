from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Product, Review
from .forms import ReviewForm


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
    reviews = product.reviews.all().order_by('-created_at')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            return redirect('product_detail', category_slug=category_slug, product_slug=product_slug)
    else:
        form = ReviewForm()
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })