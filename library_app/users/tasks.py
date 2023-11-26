from celery import shared_task

from django.core.mail import send_mail


@shared_task()
def send_welcome_email_task(email_address):
    """Sends an email when the feedback form has been submitted."""
    send_mail(
        "Привет!",
        "Рады видеть вас в нашей Маленькой библиотеке питониста! Заходите почаще!",
        "support@example.com",
        [email_address],
        fail_silently=False,
    )
