from django.db import models
from core.models import BaseModel
from library.models import BookCopy
from django.conf import settings
from django.utils import timezone
from decimal import Decimal



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
    daily_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    penalty_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.borrower.email} - {self.book_copy.book.title if self.book_copy and self.book_copy.book else 'No Book'}"


    def calculate_penalty(self):
        if self.status == 'overdue' and self.due_date and not self.returned_date:
            days_overdue = (timezone.now() - self.due_date).days
            if days_overdue > 0:
                penalty_rate = Decimal('0.01')  # 1%
                penalty = self.daily_price * penalty_rate * days_overdue
                self.penalty_amount = penalty
                self.save()
                return penalty
        return Decimal('0')

    def save(self, *args, **kwargs):
        if self.returned_date:
            self.status = 'returned'
        elif self.due_date and timezone.now() > self.due_date:
            self.status = 'overdue'
            self.calculate_penalty()
        else:
            self.status = 'active'
        super().save(*args, **kwargs)
