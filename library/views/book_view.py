from rest_framework import viewsets
from library.models import Book
from library.serializers import BookSerializer
from library.pagination import BookPagination


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
