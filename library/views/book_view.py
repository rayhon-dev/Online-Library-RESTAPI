from rest_framework import viewsets
from library.models import Book, Rating, BookCopy
from lending.models import BookReservation
from lending.serializers import BookReservationSerializer
from library.serializers import BookSerializer, RatingSerializer, BookCopySerializer
from library.pagination import BookPagination
from core.permissions import BookPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from datetime import timedelta
from django.utils import timezone


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination
    permission_classes = [BookPermission]

    @action(detail=True, methods=['post'], url_path='rate', permission_classes=[IsAuthenticated])
    def rate(self, request, pk=None):
        book = self.get_object()
        user = request.user
        rating_value = request.data.get('rating')
        review_text = request.data.get('review', '')

        if rating_value is None or not (0 <= int(rating_value) <= 5):
            return Response({"error": "Rating must be between 0 and 5"}, status=status.HTTP_400_BAD_REQUEST)

        rating_obj, created = Rating.objects.update_or_create(
            user=user,
            book=book,
            defaults={'rating': rating_value, 'review': review_text}
        )
        serializer = RatingSerializer(rating_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


    @action(detail=True, methods=['post'], url_path='reserve', permission_classes=[IsAuthenticated])
    def reserve(self, request, pk=None):
        book = self.get_object()
        user = request.user

        expires_at = timezone.now() + timedelta(days=1)

        available_copies = BookCopy.objects.filter(book=book).exclude(
            book_reservations__is_active=True,
            book_reservations__expires_at__gt=timezone.now()
        )

        if not available_copies.exists():
            return Response({"error": "No available copies to reserve."}, status=status.HTTP_400_BAD_REQUEST)

        book_copy = available_copies.first()

        reservation = BookReservation.objects.create(
            book_copy=book_copy,
            reserver=user,
            expires_at=expires_at,
            is_active=True
        )
        serializer = BookReservationSerializer(reservation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='available_copies')
    def available_copies(self, request, pk=None):
        book = self.get_object()
        available_copies = BookCopy.objects.filter(book=book).exclude(
            book_reservations__is_active=True,
            book_reservations__expires_at__gt=timezone.now()
        )
        serializer = BookCopySerializer(available_copies, many=True)
        return Response(serializer.data)