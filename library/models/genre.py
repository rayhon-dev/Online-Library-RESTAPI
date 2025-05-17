from django.db import models
from core.models import BaseModel


class Genre(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name