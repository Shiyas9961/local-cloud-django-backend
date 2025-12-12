from django.urls import reverse


def test_refresh_token(api_client, user):
    login_url = reverse("token_obtain_pair")
    refresh_url = reverse("token_refresh")

    login = api_client.post(
        login_url, {"username": user.username, "password": "password123"}
    )
    refresh = api_client.post(refresh_url, {"refresh": login.data["refresh"]})

    assert refresh.status_code == 200
    assert "access" in refresh.data
