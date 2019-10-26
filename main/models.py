from django.db import models
from django.urls import reverse_lazy


# class Registration(models.Model):
#     firs_name = models.CharField('Имя', max_length=120)
#     last_name = models.CharField('Фамилия', max_length=120)
#     image = models.ImageField('Фото', null=True, blank=True, upload_to='cover')
#
#     def __str__(self):
#         return self.firs_name
#
#     def get_absolute_url(self):
#         return reverse_lazy('author-detail', kwargs={'pk': self.pk})
