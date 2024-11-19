from celery import shared_task

@shared_task
def send_email_notification(subject, message, recipient_list):
    from django.core.mail import send_mail
    send_mail(subject, message, 'admin@example.com', recipient_list)
