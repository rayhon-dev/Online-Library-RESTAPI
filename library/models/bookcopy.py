from django.db import models
from core.models import BaseModel
from library.models import Book


class BookCopy(BaseModel):
    BOOK_CONDITIONS = [
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor')
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_copies')
    inventory_number = models.CharField(max_length=100, unique=True)
    condition = models.CharField(max_length=10, choices=BOOK_CONDITIONS)
    is_available = models.BooleanField(default=True)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} ({self.inventory_number})"

    class Meta:
        verbose_name = "Book Copy"
        verbose_name_plural = "Book Copies"