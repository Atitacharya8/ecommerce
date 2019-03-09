from django.contrib import admin

# Register your models here.
from eco.models import Category, Product, Review

admin.site.register([Category,Product,Review])