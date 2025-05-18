from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from lending.models import BookLending
from lending.serializers import BookLendingSerializer
from lending.pagination import BookLendingPagination
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminOrOperator, IsOwnerOrReadOnly
from django.utils import timezone



class BookLendingViewSet(viewsets.ModelViewSet):
    queryset = BookLending.objects.all()
    serializer_class = BookLendingSerializer
    pagination_class = BookLendingPagination

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'operator']:
            return BookLending.objects.all()
        return BookLending.objects.filter(borrower=user)

    def get_permissions(self):
        if self.action == 'overdue':
            return [IsAuthenticated(), IsAdminOrOperator()]
        elif self.request.user.role in ['admin', 'operator']:
            return [IsAuthenticated()]
        elif self.request.user.role == 'user':
            if self.action in ['create', 'list', 'retrieve']:
                return [IsAuthenticated()]
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return [IsAuthenticated()]


    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue(self, request):
        queryset = BookLending.objects.filter(status='overdue')
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True) if page is not None else self.get_serializer(queryset, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='return', permission_classes=[IsAuthenticated])
    def return_book(self, request):
        lending_id = request.data.get('lending_id')
        try:
            lending = BookLending.objects.get(id=lending_id, borrower=request.user, status='active')
        except BookLending.DoesNotExist:
            return Response({"error": "Active lending not found."}, status=status.HTTP_404_NOT_FOUND)

        lending.returned_date = timezone.now()
        lending.status = 'returned'
        lending.save()
        serializer = BookLendingSerializer(lending)
        return Response(serializer.data)