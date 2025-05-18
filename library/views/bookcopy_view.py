from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from library.models import BookCopy
from library.serializers import BookCopySerializer
from library.pagination import BookCopyPagination
from core.permissions import BookCopyPermission
from django_filters.rest_framework import DjangoFilterBackend
from library.filters import BookCopyFilter


class BookCopyViewSet(viewsets.ModelViewSet):
    queryset = BookCopy.objects.all()
    serializer_class = BookCopySerializer
    pagination_class = BookCopyPagination
    permission_classes = [BookCopyPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookCopyFilter

    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request):
        queryset = self.get_queryset().filter(is_available=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
