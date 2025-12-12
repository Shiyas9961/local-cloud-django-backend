"""Core application tasks send email."""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from backend.celery import app


@app.task(queue="email_queue")
def send_html_email(template_name, subject, to_email, context=None):
    """Send HTML email."""
    html_content = render_to_string(f"email/{template_name}", context or {})
    from_email = settings.ADMIN_EMAIL

    email = EmailMultiAlternatives(
        subject=subject,
        body="Your email client does not support HTML messages.",
        from_email=from_email,
        to=[to_email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

    return f"Email sent to {to_email}"
