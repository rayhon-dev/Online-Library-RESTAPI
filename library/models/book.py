from django.db import models
from core.models import BaseModel
from library.models import Author


class Book(BaseModel):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name='books')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    page_count = models.PositiveIntegerField()
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.title