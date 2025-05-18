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
    return User.objects.create_superuser(
        username='admin',           # qo'shildi
        email='admin@test.com',
        password='pass123',
        role='admin'
    )


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        username='user',            # qo'shildi
        email='user@test.com',
        password='pass123',
        role='user'
    )



@pytest.fixture
def genre(db):
    return Genre.objects.create(name='Sci-Fi')


@pytest.fixture
def author(db):
    return Author.objects.create(first_name='Isaac', last_name='Asimov', nationality='American')


@pytest.fixture
def book(db, genre, author):
    book = Book.objects.create(
        title='Foundation',
        genre=genre,
        isbn='1234567890123',
        language='English'
    )
    book.authors.add(author)
    return book


@pytest.fixture
def bookcopy(db, book):
    return BookCopy.objects.create(
        book=book,
        inventory_number='INV001',
        condition='good',
        is_available=True
    )


@pytest.mark.django_db
def test_bookcopy_list(api_client, regular_user, bookcopy):
    api_client.force_authenticate(user=regular_user)
    url = reverse('book_copy-list')  # router.register basename='book_copy' bo‘lsa
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['inventory_number'] == 'INV001'


@pytest.mark.django_db
def test_create_bookcopy(api_client, admin_user, book):
    api_client.force_authenticate(user=admin_user)
    url = reverse('book_copy-list')
    data = {
        'book': book.id,
        'inventory_number': 'INV002',
        'condition': 'new',
        'is_available': True
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['inventory_number'] == 'INV002'
