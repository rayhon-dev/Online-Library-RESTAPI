import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from lending.models import BookLending, BookReservation
from library.models import BookCopy, Book, Author, Genre
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal

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
def book_lending(db, bookcopy, regular_user):
    return BookLending.objects.create(
        book_copy=bookcopy,
        borrower=regular_user,
        borrowed_date=timezone.now() - timezone.timedelta(days=5),
        due_date=timezone.now() + timezone.timedelta(days=5),
        status='active',
        daily_price=Decimal('10.00'),
        penalty_amount=Decimal('0.00')
    )


@pytest.mark.django_db
def test_booklending_list_as_admin(api_client, admin_user, book_lending):
    api_client.force_authenticate(user=admin_user)
    url = reverse('book_lending-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert any(item['id'] == book_lending.id for item in response.data['results'])


@pytest.mark.django_db
def test_booklending_list_as_regular_user(api_client, regular_user, book_lending):
    api_client.force_authenticate(user=regular_user)
    url = reverse('book_lending-list')
    response = api_client.get(url)
    assert response.status_code == 200
    # Faqat o'zining lendinglarini ko'radi
    for item in response.data['results']:
        assert item['borrower'] == regular_user.id


def test_create_booklending_as_regular_user(api_client, regular_user, bookcopy):
    api_client.force_authenticate(user=regular_user)
    url = reverse('book_lending-list')
    data = {
        'book_copy': bookcopy.id,
        'borrowed_date': timezone.now().isoformat(),
        'due_date': (timezone.now() + timezone.timedelta(days=7)).isoformat(),
        'daily_price': '1.00',
        'status': 'active',
        'borrower': regular_user.id,  # Qo'shildi
    }

    response = api_client.post(url, data)
    print(response.status_code)
    print(response.data)
    assert response.status_code in [201, 403]


@pytest.mark.django_db
def test_return_book_action(api_client, regular_user, book_lending):
    api_client.force_authenticate(user=regular_user)
    url = reverse('book_lending-return-book')
    data = {'lending_id': book_lending.id}
    response = api_client.post(url, data, format='json')
    # Agar lending status 'active' bo'lsa, return qilish mumkin
    assert response.status_code == 200
    book_lending.refresh_from_db()
    assert book_lending.status == 'returned'
    assert book_lending.returned_date is not None


@pytest.mark.django_db
def test_overdue_list_as_admin(api_client, admin_user, book_lending):
    # Lendingni overdue holatiga o'tkazish uchun due_date o'tgan qilish
    book_lending.due_date = timezone.now() - timezone.timedelta(days=1)
    book_lending.save()
    api_client.force_authenticate(user=admin_user)
    url = reverse('book_lending-overdue')
    response = api_client.get(url)
    assert response.status_code == 200
    assert any(item['id'] == book_lending.id for item in response.data['results'])
