from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Category, Product, Review, Order
from .forms import ReviewForm, OrderForm
from .telegram_bot import send_order_notification


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
    review_form = ReviewForm()
    order_form = OrderForm()
    
    if request.method == 'POST':
        if 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.save()
                messages.success(request, 'Дякуємо за ваш відгук!')
                return redirect('product_detail', category_slug=category_slug, product_slug=product_slug)
        
        elif 'order_submit' in request.POST:
            order_form = OrderForm(request.POST)
            if order_form.is_valid():
                order = order_form.save(commit=False)
                order.product = product
                order.save()

                order_data = {
                    'order_id': order.id,
                    'product_name': product.name,
                    'quantity': order.quantity,
                    'customer_name': order.customer_name,
                    'phone': order.phone,
                    'address': order.address,
                    'comment': order.comment or 'Немає коментаря'
                }
                
                try:
                    send_order_notification(order_data)
                    messages.success(request, 'Ваше замовлення успішно оформлено!')
                except Exception as e:
                    messages.warning(request, 'Замовлення прийнято, але виникли проблеми з повідомленням.')
                
                return redirect('product_detail', category_slug=category_slug, product_slug=product_slug)
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'order_form': order_form
    })