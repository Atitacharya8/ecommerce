from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from eco import views

app_name = "eco"

urlpatterns = [
#password reset
path('password-reset/', auth_views.PasswordResetView.as_view(template_name='eco/password_reset.html'),
     name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='eco/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='eco/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='eco/password_reset_complete.html'),
         name='password_reset_complete'),
    path('AtitAdmin/', views.AtitAdmin, name="AtitAdmin"),
    path('category/', views.category, name="category"),
    path('product/', views.product, name="product"),
    path('feedback/', views.feedback, name="feedback"),
    path('product_create/', views.product_create_view, name="product_create"),
    path('product_list_update/', views.product_list_update, name="product_list_update"),
    path('product_list_delete/', views.product_list_delete, name="product_list_delete"),
    path('product_update/<slug>/', views.product_update_view, name="product_update"),
    path('product_delete/<slug>/', views.product_delete_view, name="product_delete"),
    path('category_list_update/', views.category_list_update, name="category_list_update"),
    path('category_list_delete/', views.category_list_delete, name="category_list_delete"),
    path('category_create/', views.category_create_view, name="category_create"),
    path('category_delete/<slug>/', views.category_delete_view, name="category_delete"),
    path('category_update/<slug>/', views.category_update_view, name="category_update"),
    path('accounts/profile/', views.profile, name="profile"),
    path('about/', views.about, name='about'),
    path('home/', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('search/', views.search, name="search"),
    path('googlemap/', views.googlemap, name='googlemap'),
    path('<slug>/cart/', views.cart, name="cart"),
    path('mycart/', views.mycart, name="mycart"),
    path('checkout/', views.checkout, name="checkout"),
    path('<slug>/', views.detail, name="detail"),
    path('categories/<slug>/', views.categories, name="categories"),
    path('api/products/', views.api_products, name="api_products"),



]
