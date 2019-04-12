from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from eco.models import Category, Product, Review,Feedback


@admin.register(Category, Product, Review,Feedback)
class CategoryAdmin(ImportExportModelAdmin):
    pass


class ProductAdmin(ImportExportModelAdmin):
    pass


class ReviewAdmin(ImportExportModelAdmin):
    pass


class FeedbackAdmin(ImportExportModelAdmin):
    pass


