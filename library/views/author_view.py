from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from library.models import Author, Book
from library.serializers import AuthorSerializer, AuthorBookSerializer
from library.pagination import AuthorPagination, AuthorBookPagination
from core.permissions import IsAdminOrReadOnly


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = AuthorPagination
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['get'], pagination_class=AuthorBookPagination)
    def books(self, request, pk=None):
        author_books = Book.objects.filter(authors__id=pk)
        page = self.paginate_queryset(author_books)
        if page is not None:
            serializer = AuthorBookSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = AuthorBookSerializer(author_books, many=True)
        return Response(serializer.data)
