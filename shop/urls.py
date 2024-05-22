from django.urls import path
from .views import (index, shop, detail, save_review, product_by_category, user_login, user_logout, user_register,
                    to_cart, cart, pay_success, pay_failed, create_checkout_sessions, save_shipping_address,
                    checkout_page, sort_by_price)

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name="index"),
    path('product-list/', shop, name="shop"),
    path('detail/<int:product_pk>/', detail, name="detail"),
    path('save-review/<int:product_pk>/', save_review, name="save_review"),
    path('by-category/<str:slug>/', product_by_category, name="by_category"),

    path('login/', user_login, name="login"),
    path('logout/', user_logout, name="logout"),
    path('register/', user_register, name="register"),

    path('reset-password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='shop/reset_done.html'),
         name="password_reset_complete"),

    path('cart/', cart, name="cart"),
    path('to-cart/<int:product_id>/<str:action>/', to_cart, name="to_cart"),

    path('payment/', create_checkout_sessions, name="payment"),
    path('payment-success/', pay_success, name="payment_success"),
    path('payment-failed/', pay_failed, name="payment_failed"),
    path('checkout/', checkout_page, name="checkout"),
    path('save-shipping-address/', save_shipping_address, name="save_shipping_address"),

    path('sort-by-price/<str:method>/', sort_by_price, name="sort_by")

]
