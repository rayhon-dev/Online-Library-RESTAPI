import pytest
from library.models import Rating, Book, Author, Genre
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='user1', email='user1@test.com', password='pass123')

@pytest.fixture
def genre(db):
    return Genre.objects.create(name='Mystery')

@pytest.fixture
def author(db):
    return Author.objects.create(first_name='Agatha', last_name='Christie', nationality='British')

@pytest.fixture
def book(db, genre, author):
    book = Book.objects.create(
        title='Murder on the Orient Express',
        genre=genre,
        isbn='1231231231231',
        language='English'
    )
    book.authors.add(author)
    return book

@pytest.mark.django_db
def test_create_rating(db, user, book):
    rating = Rating.objects.create(user=user, book=book, rating=5, review='Excellent!')
    assert rating.rating == 5
    assert rating.review == 'Excellent!'
    assert rating.book == book
    assert rating.user == user
