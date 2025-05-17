from django.contrib import admin
from .models import Genre, Author, Book, BookCopy


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'nationality', 'birth_date')
    search_fields = ('first_name', 'last_name', 'nationality')
    list_filter = ('nationality', 'birth_date')
    ordering = ('last_name', 'first_name')


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'published_date', 'language')
    search_fields = ('title', 'isbn', 'language', 'authors__first_name', 'authors__last_name')
    list_filter = ('genre', 'language', 'published_date')
    ordering = ('title',)


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ('inventory_number', 'book', 'condition', 'is_available', 'added_date')
    search_fields = ('inventory_number', 'book__title')
    list_filter = ('condition', 'is_available', 'added_date')
    ordering = ('inventory_number',)
