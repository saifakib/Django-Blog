from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Author, Category, Article


# Register your models here.

class AuthorModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__", "details"]

    class Meta:
        Model = Author


class ArticleModel(admin.ModelAdmin):
    list_display = ["__str__", "posted_on"]
    search_fields = ["__str__", "details"]
    list_per_page = 10
    list_filter = ["posted_on", "category"]

    class Meta:
        Model = Article


class CategoryModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10

    class Meta:
        Model = Category


admin.site.register(Article, ArticleModel)
admin.site.register(Author, AuthorModel)
admin.site.register(Category, CategoryModel)