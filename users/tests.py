import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import CustomUser, UserProfile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def regular_user(db):
    user = CustomUser.objects.create_user(
        username='user',
        email='user@test.com',
        password='pass123',
        role='user'
    )
    UserProfile.objects.create(user=user, bio='Hello user')  # profil bir marta yaratiladi
    return user

@pytest.fixture
def admin_user(db):
    user = CustomUser.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='pass123',
        role='admin'
    )
    UserProfile.objects.create(user=user, bio='Admin profile')
    return user

@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse('register')
    data = {
        'username': 'newuser',
        'email': 'newuser@test.com',
        'password': 'newpass123',
        'password2': 'newpass123',
        'first_name': 'New',
        'last_name': 'User'
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert 'email' in response.data

@pytest.mark.django_db
def test_login_user(api_client, regular_user):
    url = reverse('token_obtain_pair')
    data = {
        'email': regular_user.email,
        'password': 'pass123'
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert 'access' in response.data

@pytest.mark.django_db
def test_get_current_user(api_client, regular_user):
    url = reverse('current-user')
    api_client.force_authenticate(user=regular_user)
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['email'] == regular_user.email

@pytest.mark.django_db
def test_get_user_list_admin(api_client, admin_user):
    url = reverse('user-list')
    api_client.force_authenticate(user=admin_user)
    response = api_client.get(url)
    assert response.status_code == 200
    assert isinstance(response.data, list) or 'results' in response.data  # paginate bo‘lsa results bor

@pytest.mark.django_db
def test_get_user_list_regular_user_forbidden(api_client, regular_user):
    url = reverse('user-list')
    api_client.force_authenticate(user=regular_user)
    response = api_client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_user_profile_detail_and_update(api_client, regular_user):
    url = reverse('user-profile', args=[regular_user.username])
    api_client.force_authenticate(user=regular_user)
    response = api_client.get(url)
    assert response.status_code == 200
    data = {'bio': 'Updated bio'}
    response = api_client.patch(url, data)
    assert response.status_code == 200
    assert response.data['bio'] == 'Updated bio'

@pytest.mark.django_db
def test_user_profile_list_for_admin_and_operator(api_client, admin_user):
    url = reverse('profile-list')
    api_client.force_authenticate(user=admin_user)
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_profile_list_for_regular_user_forbidden(api_client, regular_user):
    url = reverse('profile-list')
    api_client.force_authenticate(user=regular_user)
    response = api_client.get(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_logout(api_client, regular_user):
    url = reverse('logout')
    api_client.force_authenticate(user=regular_user)
    login_url = reverse('token_obtain_pair')
    login_data = {'email': regular_user.email, 'password': 'pass123'}
    login_resp = api_client.post(login_url, login_data)
    refresh_token = login_resp.data.get('refresh')
    response = api_client.post(url, {'refresh': refresh_token})
    assert response.status_code == 205
