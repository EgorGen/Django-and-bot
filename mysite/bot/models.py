from django.db import models

class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name = 'ID пользователя',
        unique = True,
    )
    name = models.TextField(
        verbose_name = 'Имя пользователя',
    )

    def __str__(self):
        return f'#{self.external_id}{self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Message(models.Model):
    profile = models.ForeignKey(
        to = 'bot.Profile',
        verbose_name = 'Профиль',
        on_delete = models.PROTECT,
    )
    text = models.TextField(
        verbose_name = 'Город',
    )
    created_at = models.DateTimeField(
        verbose_name = 'Время получения',
        auto_now_add = True,
    )

    send = models.TextField(
        verbose_name = 'Рассылка',
    )

    def __str__(self):
        return f'Сообщение {self.pk}{self.profile}'
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'