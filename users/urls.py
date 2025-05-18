from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('users/me/', views.CurrentUserView.as_view(), name='current-user'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('profiles/', views.UserProfileListView.as_view(), name='profile-list'),
    path('profile/<str:username>/', views.UserProfileView.as_view(), name='user-profile'),
    path('auth/logout/', views.UserLogoutView.as_view(), name='logout'),
]