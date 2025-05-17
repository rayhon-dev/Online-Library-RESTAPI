from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from lending.models import BookLending
from lending.serializers import BookLendingSerializer
from lending.pagination import BookLendingPagination


class BookLendingViewSet(viewsets.ModelViewSet):
    queryset = BookLending.objects.all()
    serializer_class = BookLendingSerializer
    pagination_class = BookLendingPagination

    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue(self, request):
        queryset = BookLending.objects.filter(status='overdue')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)
