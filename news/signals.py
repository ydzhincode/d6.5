from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post, PostCategory
from django.core.mail import send_mail
from django.shortcuts import redirect

@receiver(m2m_changed, sender=Post)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        subscribers = instance.category.values('subscribers__email', 'subscribers__username')


        # Отправляем письмо каждому подписчику
        for subscriber in subscribers:

            send_mail(
                subject=f'Здравствуй, {subscriber}. Новая статья в твоём любимом разделе!',

                message=f'Добавлена новость с заголовком: {title}\n{text}',
                from_email='managernewssk@mail.ru',

                recipient_list=[subscriber.email]
            )

        return redirect('news_list')

