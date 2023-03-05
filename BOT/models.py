from django.db import models

class UsersList(models.Model):
    groupName = models.TextField(
        verbose_name='Название группы'
    )
    idUser = models.TextField(
        verbose_name='ID аккаунта Телеграм'
    )
    nameUser = models.TextField(
        verbose_name='Имя пользователя'
    )
    alertStatus = models.TextField(
        verbose_name='Статус оповещений'
    )

    def __str__(self):
        return f'#{self.groupName} {self.idUser} {self.nameUser} {self.alertStatus}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'