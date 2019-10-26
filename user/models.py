from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserCustom(User, models.Model):
    user = models.OneToOneField(User, parent_link=True, related_name="custom", on_delete=models.CASCADE)
    phone = models.CharField('Телефон', help_text='+375**-***-**-**', max_length=16)
    avatar = models.ImageField('Фото профиля', null=True, blank=True, upload_to='avatar')
    country = models.CharField('Страна', null=True, blank=True, max_length=120)
    city = models.CharField('Город', null=True, blank=True, max_length=80)
    street = models.CharField('Улица, дом, квартира', null=True, blank=True, max_length=120)
    index = models.IntegerField('Индекс', null=True, blank=True)
    info = models.TextField('Дополнительна информация', null=True, blank=True, max_length=200)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
