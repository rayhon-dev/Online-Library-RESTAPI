from django.db import models
from core.models import BaseModel
from library.models import BookCopy
from django.conf import settings


class BookLending(BaseModel):
    STATUS = [
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
    ]

    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='book_lendings')
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='book_lendings')
    borrowed_date = models.DateTimeField()
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return f"{self.borrower.email} - {self.book_copy.book.title if self.book_copy and self.book_copy.book else 'No Book'}"
