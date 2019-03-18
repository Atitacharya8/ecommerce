from django.contrib import admin
from django.urls import path

from eco import views

app_name = "eco"

urlpatterns = [
    path('accounts/profile/',views.profile,name="profile"),
    path('about/',views.about,name='about'),
    path('home/', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('search/', views.search, name="search"),
    path('googlemap/',views.googlemap,name='googlemap'),
    path('<slug>/cart/', views.cart, name="cart"),
    path('mycart/', views.mycart, name="mycart"),
    path('checkout/', views.checkout, name="checkout"),
    path('<slug>/', views.detail, name="detail"),
    path('categories/<slug>/', views.categories, name="categories"),
    path('api/products/', views.api_products, name="api_products"),


]
