import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from lending.models import BookReservation
from library.models import BookCopy, Book, Author, Genre
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
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

@pytest.fixture
def book_reservation(db, bookcopy, regular_user):
    return BookReservation.objects.create(
        book_copy=bookcopy,
        reserver=regular_user,
        expires_at=timezone.now() + timezone.timedelta(days=1),
        is_active=True
    )


@pytest.mark.django_db
def test_bookreservation_list_as_admin(api_client, admin_user, book_reservation):
    api_client.force_authenticate(user=admin_user)
    url = reverse('book_reservation-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert any(item['id'] == book_reservation.id for item in response.data['results'])


@pytest.mark.django_db
def test_bookreservation_list_as_regular_user(api_client, regular_user, book_reservation):
    api_client.force_authenticate(user=regular_user)
    url = reverse('book_reservation-list')
    response = api_client.get(url)
    assert response.status_code == 200
    for item in response.data['results']:
        assert item['reserver'] == regular_user.id


@pytest.mark.django_db
def test_create_bookreservation_as_regular_user(api_client, regular_user, bookcopy):
    api_client.force_authenticate(user=regular_user)
    url = reverse('book_reservation-list')
    data = {
        'book_copy': bookcopy.id,
        'expires_at': (timezone.now() + timezone.timedelta(days=1)).isoformat(),
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code in [201, 403]


@pytest.mark.django_db
def test_overdue_list_as_admin(api_client, admin_user, book_reservation):
    book_reservation.expires_at = timezone.now() - timezone.timedelta(days=1)
    book_reservation.save()
    api_client.force_authenticate(user=admin_user)
    url = reverse('book_reservation-overdue')
    response = api_client.get(url)
    assert response.status_code == 200
    assert any(item['id'] == book_reservation.id for item in response.data['results'])


@pytest.mark.django_db
def test_my_reservations_as_user(api_client, regular_user, book_reservation):
    api_client.force_authenticate(user=regular_user)
    url = reverse('book_reservation-my_reservations')
    response = api_client.get(url)
    assert response.status_code == 200
    for item in response.data['results']:
        assert item['reserver'] == regular_user.id
