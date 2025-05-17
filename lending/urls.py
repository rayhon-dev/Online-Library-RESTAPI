from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'lendings', views.BookLendingViewSet, basename='book_lending')
router.register(r'reservations', views.BookReservationViewSet, basename='book_reservation')


urlpatterns = [
    path('', include(router.urls)),
]
