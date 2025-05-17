from django.db import models
from core.models import BaseModel
from library.models import BookCopy


class BookReservation(BaseModel):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    reserver_name = models.CharField(max_length=255)
    reserver_email = models.EmailField()
    reserved_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Reservation by {self.reserver_name} for {self.book_copy.inventory_number}"