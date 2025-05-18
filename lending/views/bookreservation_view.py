from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from lending.models import BookReservation
from lending.serializers import BookReservationSerializer
from lending.pagination import BookReservationPagination
from core.permissions import BookReservationPermission
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


class BookReservationViewSet(viewsets.ModelViewSet):
    queryset = BookReservation.objects.all()
    serializer_class = BookReservationSerializer
    pagination_class = BookReservationPagination
    permission_classes = [BookReservationPermission]


    def perform_create(self, serializer):
        serializer.save(
            reserver=self.request.user,
            expires_at=timezone.now() + timezone.timedelta(days=1)
        )

    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue(self, request):
        now = timezone.now()
        queryset = BookReservation.objects.filter(expires_at__lt=now, is_active=True)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(queryset,many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='my', permission_classes=[IsAuthenticated])
    def my_reservations(self, request):
        user = request.user
        reservations = self.queryset.filter(reserver=user, is_active=True)
        page = self.paginate_queryset(reservations)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(reservations, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)
