from rest_framework import viewsets, permissions
from library.models import Rating
from library.serializers import RatingSerializer
from library.pagination import RatingPagination
from django_filters.rest_framework import DjangoFilterBackend
from library.filters import RatingFilter


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = RatingPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RatingFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'admin':
            return Rating.objects.all()
        return Rating.objects.filter(user=user)
