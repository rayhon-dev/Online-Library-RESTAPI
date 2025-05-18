import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from library.models import Book, Author, Genre, BookCopy
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='pass123',
        role='admin'
    )


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        username='user',
        email='user@test.com',
        password='pass123',
        role='user'
    )


@pytest.fixture
def genre(db):
    return Genre.objects.create(name="Fiction")


@pytest.fixture
def authors(db):
    return [
        Author.objects.create(first_name="John", last_name="Doe", nationality="USA"),
        Author.objects.create(first_name="Jane", last_name="Smith", nationality="UK"),
    ]


@pytest.fixture
def books(db, genre, authors):
    book1 = Book.objects.create(
        title='Book One',
        genre=genre,
        isbn='1234567890123',
        published_date='2020-01-01',
        language='English'
    )
    book1.authors.set(authors)

    book2 = Book.objects.create(
        title='Book Two',
        genre=genre,
        isbn='1234567890124',
        published_date='2021-01-01',
        language='English'
    )
    book2.authors.set(authors[:1])

    return [book1, book2]


@pytest.mark.django_db
def test_book_list(api_client, regular_user, books):
    url = reverse('book-list')
    api_client.force_authenticate(user=regular_user)
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == len(books)


@pytest.mark.django_db
def test_book_detail(api_client, regular_user, books):
    book = books[0]
    url = reverse('book-detail', args=[book.id])
    api_client.force_authenticate(user=regular_user)
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == book.id
    assert response.data['title'] == book.title


@pytest.mark.django_db
def test_create_book_admin(api_client, admin_user, genre, authors):
    url = reverse('book-list')
    api_client.force_authenticate(user=admin_user)

    data = {
        'title': 'New Book',
        'genre': genre.id,
        'isbn': '9876543210987',
        'published_date': '2023-01-01',
        'language': 'English',
        'authors': [author.id for author in authors],
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['title'] == 'New Book'


@pytest.mark.django_db
def test_create_book_non_admin(api_client, regular_user, genre, authors):
    url = reverse('book-list')
    api_client.force_authenticate(user=regular_user)

    data = {
        'title': 'Unauthorized Book',
        'genre': genre.id,
        'isbn': '1111111111111',
        'published_date': '2023-01-01',
        'language': 'English',
        'authors': [author.id for author in authors],
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == 403  # Permission denied


@pytest.mark.django_db
def test_update_book_admin(api_client, admin_user, books, genre):
    book = books[0]
    url = reverse('book-detail', args=[book.id])
    api_client.force_authenticate(user=admin_user)

    data = {
        'title': 'Updated Title',
        'genre': genre.id,
        'isbn': book.isbn,
        'published_date': book.published_date,
        'language': book.language,
        'authors': [author.id for author in book.authors.all()],
    }

    response = api_client.put(url, data, format='json')
    assert response.status_code == 200
    assert response.data['title'] == 'Updated Title'


@pytest.mark.django_db
def test_delete_book_admin(api_client, admin_user, books):
    book = books[0]
    url = reverse('book-detail', args=[book.id])
    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_rate_book(api_client, regular_user, books):
    book = books[0]
    url = reverse('book-rate', args=[book.id])
    api_client.force_authenticate(user=regular_user)

    data = {'rating': 4, 'review': 'Great book!'}
    response = api_client.post(url, data, format='json')

    assert response.status_code in (200, 201)
    assert response.data['rating'] == 4


@pytest.mark.django_db
def test_reserve_book(api_client, regular_user, books):
    book = books[0]
    BookCopy.objects.create(
        book=book,
        inventory_number='INV12345',
        condition='good',
        is_available=True
    )

    url = reverse('book-reserve', args=[book.id])
    api_client.force_authenticate(user=regular_user)
    response = api_client.post(url)

    assert response.status_code == 201
    assert 'id' in response.data


@pytest.mark.django_db
def test_available_copies(api_client, regular_user, books):
    book = books[0]
    copy = BookCopy.objects.create(
        book=book,
        inventory_number='INV67890',
        condition='new',
        is_available=True
    )

    url = reverse('book-available-copies', args=[book.id])
    api_client.force_authenticate(user=regular_user)
    response = api_client.get(url)

    assert response.status_code == 200
    assert any(item['inventory_number'] == copy.inventory_number for item in response.data)
