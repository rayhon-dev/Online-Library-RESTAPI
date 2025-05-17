from django.contrib import admin
from .models import BookLending, BookReservation


@admin.register(BookLending)
class BookLendingAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'book_copy', 'borrowed_date', 'due_date', 'returned_date', 'status')
    list_filter = ('status', 'borrowed_date', 'due_date')
    search_fields = ('borrower__email', 'book_copy__book__title')
    ordering = ('-borrowed_date',)


@admin.register(BookReservation)
class BookReservationAdmin(admin.ModelAdmin):
    list_display = ('reserver_name', 'book_copy', 'reserved_at', 'expires_at', 'is_active')
    list_filter = ('is_active', 'reserved_at', 'expires_at')
    search_fields = ('reserver_name', 'reserver_email', 'book_copy__book__title')
    ordering = ('-reserved_at',)
