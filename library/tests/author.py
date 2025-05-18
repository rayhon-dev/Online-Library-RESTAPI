import pytest
from django.urls import reverse
from library.models import Author
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username='admin', email='admin@test.com', password='pass123')


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(username='user', email='user@test.com', password='pass123')


@pytest.fixture
def authors(db):
    return [
        Author.objects.create(first_name='John', last_name='Doe', nationality='USA'),
        Author.objects.create(first_name='Jane', last_name='Smith', nationality='UK'),
    ]


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.mark.django_db
def test_author_list(api_client, authors):
    url = reverse('author-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == len(authors)


@pytest.mark.django_db
def test_author_retrieve(api_client, authors):
    url = reverse('author-detail', args=[authors[0].id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == authors[0].id
    assert response.data['first_name'] == authors[0].first_name


@pytest.mark.django_db
def test_create_author_admin(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('author-list')
    data = {
        'first_name': 'New',
        'last_name': 'Author',
        'nationality': 'France',
        'bio': 'Some bio',
        'birth_date': '1980-01-01'
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['first_name'] == 'New'


@pytest.mark.django_db
def test_create_author_non_admin(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    url = reverse('author-list')
    data = {
        'first_name': 'New',
        'last_name': 'Author',
        'nationality': 'France',
    }
    response = api_client.post(url, data)
    assert response.status_code == 403  # Permission denied


@pytest.mark.django_db
def test_update_author_admin(api_client, admin_user, authors):
    api_client.force_authenticate(user=admin_user)
    url = reverse('author-detail', args=[authors[0].id])
    data = {
        'first_name': 'Updated',
        'last_name': 'Name',
        'nationality': 'Germany'
    }
    response = api_client.put(url, data)
    assert response.status_code == 200
    assert response.data['first_name'] == 'Updated'


@pytest.mark.django_db
def test_delete_author_admin(api_client, admin_user, authors):
    api_client.force_authenticate(user=admin_user)
    url = reverse('author-detail', args=[authors[0].id])
    response = api_client.delete(url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_author_non_admin(api_client, regular_user, authors):
    api_client.force_authenticate(user=regular_user)
    url = reverse('author-detail', args=[authors[0].id])
    response = api_client.delete(url)
    assert response.status_code == 403
