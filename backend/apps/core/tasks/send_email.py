from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from backend.celery import app


@app.task(queue="email_queue")
def send_html_email(template_name, subject, to_email, context=None):
    """
    Sends HTML email using LocalStack SES (or real SES in production).
    """

    html_content = render_to_string(f"email/{template_name}", context or {})

    email = EmailMultiAlternatives(
        subject=subject,
        body="Your email client does not support HTML messages.",
        from_email=None,
        to=[to_email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

    return f"Email sent to {to_email}"
