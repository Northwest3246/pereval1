import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from passes.models import User, Coordinates, Level, Pass

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def sample_pass():
    user = User.objects.create(
        email="test@example.com",
        fam="Иванов",
        name="Иван",
        otc="Иванович",
        phone="+79991234567"
    )
    coords = Coordinates.objects.create(
        latitude="45.3842",
        longitude="7.1525",
        height=1200
    )
    level = Level.objects.create(
        winter="",
        summer="1А",
        autumn="1А",
        spring=""
    ) return Pass.objects.create(
        beauty_title="пер.",
        title="Тестовый перевал",
        other_titles="Альтернативное название",
        connect="",
        add_time="2024-01-01T12:00:00Z",
        user=user, coords=coords,
        level=level,
        status="new"
    )

@pytest.mark.django_db
def test_submit_data(api_client):
    data = {
        "beauty_title": "пер. ",
        "title": "Пхия",
        "other_titles": "Триев",
        "connect": "",
        "add_time": "2021-09-22T13:18:13",
        "user": {
            "email": "test2@example.com",
            "fam": "Петров",
            "name": "Петр",
            "otc": "Петрович",
            "phone": "+79997654321"
        },
        "coords": {
            "latitude": "45.3842",
            "longitude": "7.1525",
            "height": 1200
        },
        "level": {
            "winter": "",
            "summer": "1А",
            "autumn": "1А",
            "spring": ""
        },
        "images": []
    }
    url = reverse('passes:submit_data')
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert response.data['status'] == 200
    assert response.data['id'] is not None

@pytest.mark.django_db
def test_get_pass(api_client, sample_pass):
    url = reverse('passes:get_pass', kwargs={'pk': sample_pass.id})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['title'] == "Тестовый перевал"

@pytest.mark.django_db
def test_edit_pass(api_client, sample_pass):
    url = reverse('passes:edit_pass', kwargs={'pk': sample_pass.id})
    data = {
        "title": "Обновлённый перевал",
        "beauty_title": "пер. Новый"
    }
    response = api_client.patch(url, data, format='json')
    assert response.status_code == 200
    assert response.data['state'] == 1
    sample_pass.refresh_from_db()
    assert sample_pass.title == "Обновлённый перевал"

@pytest.mark.django_db
def test_edit_pass_rejected_status(api_client, sample_pass):
    sample_pass.status = "accepted"
    sample_pass.save()
    url = reverse('passes:edit_pass', kwargs={'pk': sample_pass.id})
    data = {"title": "Попытка изменить"}
    response = api_client.patch(url, data, format='json')
    assert response.status_code == 400
    assert response.data['state'] == 0
    assert "Редактирование запрещено" in response.data['message']

@pytest.mark.django_db
def test_get_passes_by_user(api_client, sample_pass):
    url = reverse('passes:get_passes_by_user') + '?user__email=test@example.com'
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['data']) == 1
    assert response.data['data'][0]['title'] == "Тестовый перевал"

@pytest.mark.django_db
def test_submit_and_retrieve(api_client):
    data = {
        "beauty_title": "пер. ",
        "title": "Интеграционный тест",
        "other_titles": "",
        "connect": "",
        "add_time": "2024-01-01T12:00:00Z",
        "user": {
            "email": "integration@test.com",
            "fam": "Тестов",
            "name": "Тест",
            "otc": "",
            "phone": "+79998887766"
        },
        "coords": {
            "latitude": "50.0000",
            "longitude": "10.0000",
            "height": 1500
        },
        "level": {
            "winter": "",
            "summer": "1А",
            "autumn": "",
            "spring": ""
        },
        "images": []
    }
    url = reverse('passes:submit_data')
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    pass_id = response.data['id']

    url_get = reverse('passes:get_pass', kwargs={'pk': pass_id})
    response_get = api_client.get(url_get)
    assert response_get.status_code == 200
    assert response_get.data['title'] == "Интеграционный тест"
    assert response_get.data['user']['email'] == "integration@test.com"