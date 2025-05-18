from django.db import models
from django.conf import settings
from core.models import BaseModel


class Rating(BaseModel):
    RATING_CHOICES = [(i, str(i)) for i in range(6)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'book']
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rating}★"

