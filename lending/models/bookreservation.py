from django.db import models
from core.models import BaseModel
from library.models import BookCopy
from django.conf import settings


class BookReservation(BaseModel):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    reserver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='book_reservations')
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Reservation by {self.reserver.username} for {self.book_copy.inventory_number}"
