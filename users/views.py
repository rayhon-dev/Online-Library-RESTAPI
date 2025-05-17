from rest_framework import generics
from .models import UserProfile
from .serializers import CustomUserSerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    # permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    # filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    # search_fields = ['bio', 'user__username', 'user__email', 'user__first_name', 'user__last_name']
    lookup_field = 'user__username'

    def retrieve(self, request, *args, **kwargs):
        username = self.kwargs.get('user__username')
        if username:
            user_profile = UserProfile.objects.filter(user__username=username).first()
        else:
            user_profile = UserProfile.objects.filter(user=request.user).first()

        if not user_profile:
            raise NotFound(detail="Profile not found.")

        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
