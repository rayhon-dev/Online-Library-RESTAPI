from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'copies', views.BookCopyViewSet, basename='book_copy')
router.register(r'genres', views.GenreViewSet, basename='genre')



urlpatterns = [
    path('', include(router.urls)),
]
