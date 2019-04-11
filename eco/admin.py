from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from eco.models import Category, Product, Review


@admin.register(Category, Product, Review)
class CategoryAdmin(ImportExportModelAdmin):
    pass


class ProductAdmin(ImportExportModelAdmin):
    pass


class ReviewAdmin(ImportExportModelAdmin):
    pass


