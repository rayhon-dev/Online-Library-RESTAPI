import django_filters
from library.models import Book, BookCopy, Genre, Author, Rating


class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    birth_date = django_filters.DateFilter()

    class Meta:
        model = Author
        fields = ['name', 'birth_date']

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    genre = django_filters.CharFilter(field_name='genre__name', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='authors__name', lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title', 'genre', 'author']


class BookCopyFilter(django_filters.FilterSet):
    book_title = django_filters.CharFilter(field_name='book__title', lookup_expr='icontains')
    is_available = django_filters.BooleanFilter()

    class Meta:
        model = BookCopy
        fields = ['is_available', 'book_title']


class GenreFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Genre
        fields = ['name']


class RatingFilter(django_filters.FilterSet):
    rating = django_filters.NumberFilter(field_name='rating')
    book = django_filters.NumberFilter(field_name='book__id')

    class Meta:
        model = Rating
        fields = ['rating', 'book']