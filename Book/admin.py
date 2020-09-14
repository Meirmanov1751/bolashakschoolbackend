from django.contrib import admin
from .models import Book, BookImages
# Register your models here.

class BookImageInline(admin.TabularInline):
    model = BookImages

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [BookImageInline]