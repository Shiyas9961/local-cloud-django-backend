from django.urls import reverse


def test_login(api_client, user):
    url = reverse("token_obtain_pair")

    response = api_client.post(
        url, {"username": user.username, "password": "password123"}
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data
