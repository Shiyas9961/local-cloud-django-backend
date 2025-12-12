from backend.apps.core.tasks.send_email import send_html_email


def test_send_html_email(settings, mocker):
    mocker.patch("django.core.mail.EmailMultiAlternatives.send", return_value=True)

    result = send_html_email(
        template_name="test_template.html",
        subject="Test Subject",
        to_email="test@example.com",
    )

    assert "Email sent" in result
