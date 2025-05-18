import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from library.models import Genre
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
def genres(db):
    return [
        Genre.objects.create(name='Fiction', description='Fiction books'),
        Genre.objects.create(name='Science', description='Science books'),
    ]


@pytest.mark.django_db
def test_genre_list(api_client, regular_user, genres):
    url = reverse('genre-list')
    api_client.force_authenticate(user=regular_user)

    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data['results']) == len(genres)
    assert any(g['name'] == 'Fiction' for g in response.data['results'])


@pytest.mark.django_db
def test_create_genre_admin(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('genre-list')
    data = {
        'name': 'History',
        'description': 'Historical books'
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['name'] == 'History'
    assert Genre.objects.filter(name='History').exists()


@pytest.mark.django_db
def test_create_genre_non_admin(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    url = reverse('genre-list')
    data = {'name': 'Unauthorized'}

    response = api_client.post(url, data, format='json')
    assert response.status_code == 403
    assert not Genre.objects.filter(name='Unauthorized').exists()
