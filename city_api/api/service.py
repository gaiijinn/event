from django.core.mail import send_mail
from django.conf import settings


def successful_entry(event: object):
    send_mail(
        f'Поздравляю, вы успешно запись на {event.event.event_name}',
        f'Событие начнеться {event.event.date} в {event.event.begin_time} по Киевскому времени! Стоимость входа - {event.event.price}',
        f'{settings.EMAIL_HOST_USER}',
        [event.event.user.email],
        False
    )
