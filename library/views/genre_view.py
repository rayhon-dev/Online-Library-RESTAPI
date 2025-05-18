from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from library.models import Genre, Book
from library.serializers import GenreSerializer, AuthorBookSerializer
from library.pagination import GenrePagination, GenreBookPagination
from core.permissions import GenrePermission


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = GenrePagination
    permission_classes = [GenrePermission]


    @action(detail=True, methods=['get'], url_path='books', pagination_class=GenreBookPagination)
    def books(self, request, pk=None):
        books = Book.objects.filter(genre__id=pk)
        page = self.paginate_queryset(books)
        serializer = AuthorBookSerializer(page, many=True) if page is not None else AuthorBookSerializer(books, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)
