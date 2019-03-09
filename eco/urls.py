
from django.contrib import admin
from django.urls import path

from eco import views
app_name="eco"

urlpatterns = [
    path("",views.home,name="home"),
    path('<slug>/',views.detail,name="detail"),
    path("search/",views.search,name="search"),
    path("<slug>/cart/",views.cart,name="cart"),
    path("mycart/",views.mycart,name="mycart"),
    path("checkout/",views.checkout,name="checkout"),
    path("categories/<slug>/",views.categories,name="categories"),


]
