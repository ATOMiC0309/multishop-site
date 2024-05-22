from django.shortcuts import render, redirect

# Create your views here.
from .models import Category, Subcategory, Product, Review, Customer
from .forms import ReviewForm, RegisterForm, LoginForm, ShippingAddressForm
from django.contrib import messages
from django.contrib.auth import login, logout
from .utils import CartAuthenticatedUser
from django.http import HttpRequest, HttpResponse
import stripe
from django.urls import reverse
from multishop import settings


def index(request):
    context = {
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'products': Product.objects.all()[:8],
        'index_page_status': 'active',
    }
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        context['order_count'] = cart_info['cart_total_quantity']

    return render(request, 'shop/index.html', context=context)


def shop(request):
    context = {
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'products': Product.objects.all(),
        'shop_page_status': 'active',
    }
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        context['order_count'] = cart_info['cart_total_quantity']
    return render(request, 'shop/shop.html', context=context)


def detail(request, product_pk):
    product = Product.objects.get(pk=product_pk)
    context = {
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'product': product,
        'form': ReviewForm(),
        'reviews': Review.objects.filter(product=product).order_by('-pk'),
    }
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        context['order_count'] = cart_info['cart_total_quantity']

    return render(request, 'shop/detail.html', context=context)


def save_review(request, product_pk):
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        product = Product.objects.get(pk=product_pk)
        review.product = product
        review.author = request.user
        review.save()
        messages.success(request, "Sizning izohingiz saqlandi!")
        return redirect('detail', product_pk=product_pk)
    else:
        messages.error(request, "Maydonlar xato to'ldirildi!")
        return redirect('detail', product_pk=product_pk)


def product_by_category(request, slug):
    category = Subcategory.objects.get(slug=slug)
    context = {
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'products': Product.objects.filter(subcategory=category),
        'shop_page_status': 'active',
    }
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        context['order_count'] = cart_info['cart_total_quantity']
    return render(request, 'shop/shop.html', context=context)


def user_logout(request):
    """This is for logout"""

    logout(request)
    return redirect('login')


def user_login(request):
    """This is for login"""

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successfully!")
            return redirect('index')

        if form.errors:
            messages.error(request, "Check that the fields are correct!")

    form = LoginForm()
    context = {
        'form': form,
        'title': 'Sign in'
    }
    return render(request, 'shop/login.html', context=context)


def user_register(request):
    """This is for sing up"""

    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "You can log in by entering your username and password.")
            return redirect('login')

        if form.errors:
            messages.error(request, "Check that the fields are correct!")

    form = RegisterForm()
    context = {
        'form': form,
        'title': 'Sign up'
    }
    return render(request, 'shop/register.html', context=context)


def cart(request):
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()

        context = {
            'order_products': cart_info['order_products'],
            'cart_total_price': cart_info['cart_total_price'],
            'order_count': cart_info['cart_total_quantity'],
            'order': cart_info['order'],

        }
        return render(request, 'shop/cart.html', context=context)
    else:
        return redirect('login')


def to_cart(request: HttpRequest, product_id, action):
    if request.user.is_authenticated:
        CartAuthenticatedUser(request, product_id=product_id, action=action)
        page = request.META.get('HTTP_REFERER')
        return redirect(page)

    else:
        return redirect('login')


def create_checkout_sessions(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_cart = CartAuthenticatedUser(request)
    cart_info = user_cart.get_cart_info()
    total_price = cart_info['cart_total_price']
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Online shop products'
                },
                'unit_amount': int(total_price * 100)
            },
            'quantity': 1
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse("payment_success")),
        cancel_url=request.build_absolute_uri(reverse("payment_failed"))
    )
    return redirect(session.url, 303)


def pay_success(request):
    user_cart = CartAuthenticatedUser(request)
    cart_info = user_cart.get_cart_info()
    order = cart_info['order']
    order_products = cart_info['order_products']
    for product in order_products:
        product.delete()
    messages.success(request, "You order accepted!")
    # order.delete()
    return render(request, 'shop/payment_success.html')


def pay_failed(request):
    messages.error(request, "You order failed!")
    return render(request, 'shop/payment_failed.html')


def checkout_page(request):
    cart_info = CartAuthenticatedUser(request).get_cart_info()
    form = ShippingAddressForm()
    context = {
        'order_products': cart_info['order_products'],
        'cart_total_price': cart_info['cart_total_price'],
        'order_count': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'form': form,

    }

    return render(request, 'shop/checkout.html', context=context)


def save_shipping_address(request):
    if request.user.is_authenticated:
        form = ShippingAddressForm(data=request.POST)
        if form.is_valid():
            user_cart = CartAuthenticatedUser(request).get_cart_info()
            shipping_address = form.save(commit=False)
            shipping_address.customer, created = Customer.objects.get_or_create(user=request.user)
            shipping_address.order = user_cart['order']
            shipping_address.save()
            messages.success(request, "You are checked!")
            return redirect('payment')

        messages.error(request, "Fields are invalid!")
        return redirect('checkout')
    else:
        messages.warning(request, "Please login first to comment!")
        return redirect('login')


def sort_by_price(request, method):
    if method == "high":
        method = "-price"
        status = 1
    elif method == "low":
        status = 2
        method = "price"
    else:
        status = 3
        method = "pk"

    context = {
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'products': Product.objects.all().order_by(method),
        'shop_page_status': 'active',
        'status': status
    }
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        context['order_count'] = cart_info['cart_total_quantity']
    return render(request, 'shop/shop.html', context=context)
