from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from lending.models import BookReservation
from lending.serializers import BookReservationSerializer
from lending.pagination import BookReservationPagination


class BookReservationViewSet(viewsets.ModelViewSet):
    queryset = BookReservation.objects.all()
    serializer_class = BookReservationSerializer
    pagination_class = BookReservationPagination

    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue(self, request):
        queryset = BookReservation.objects.filter(status='overdue')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)
