import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from library.models import Author, Book
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    user = User.objects.create_superuser(username='admin', email='admin@test.com', password='pass123')
    return user


@pytest.fixture
def regular_user(db):
    user = User.objects.create_user(username='user', email='user@test.com', password='pass123')
    return user


@pytest.fixture
def authors(db):
    return [
        Author.objects.create(name='Author 1'),
        Author.objects.create(name='Author 2'),
    ]


@pytest.fixture
def books(authors):
    book1 = Book.objects.create(title='Book 1')
    book1.authors.add(authors[0])
    book2 = Book.objects.create(title='Book 2')
    book2.authors.add(authors[0])
    book3 = Book.objects.create(title='Book 3')
    book3.authors.add(authors[1])
    return [book1, book2, book3]


@pytest.mark.django_db
def test_author_list(api_client, authors):
    url = reverse('author-list')  # DRF default router name: modelname-list
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == len(authors)


@pytest.mark.django_db
def test_author_retrieve(api_client, authors):
    url = reverse('author-detail', args=[authors[0].id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == authors[0].id


@pytest.mark.django_db
def test_books_custom_action(api_client, authors, books):
    url = reverse('author-books', args=[authors[0].id])  # custom action 'books'
    response = api_client.get(url)
    assert response.status_code == 200
    # Check that returned books belong to the author
    for book in response.data['results']:
        assert authors[0].id in [author['id'] for author in book['authors']]


@pytest.mark.django_db
def test_create_author_admin(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('author-list')
    data = {'name': 'New Author'}
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data['name'] == 'New Author'


@pytest.mark.django_db
def test_create_author_non_admin(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    url = reverse('author-list')
    data = {'name': 'New Author'}
    response = api_client.post(url, data)
    assert response.status_code == 403  # Permission denied


@pytest.mark.django_db
def test_update_author_admin(api_client, admin_user, authors):
    api_client.force_authenticate(user=admin_user)
    url = reverse('author-detail', args=[authors[0].id])
    data = {'name': 'Updated Author'}
    response = api_client.put(url, data)
    assert response.status_code == 200
    assert response.data['name'] == 'Updated Author'


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
