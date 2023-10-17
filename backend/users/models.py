# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import Constant


class User(AbstractUser):
    email = models.EmailField(
        max_length=Constant.max_length_email_user.value,
        unique=True,
        blank=False,
        null=False
    )
    username = models.CharField(
        max_length=Constant.max_length_username_user.value,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        max_length=Constant.max_length_first_name_user.value,
        blank=False,
        null=False
    )
    last_name = models.CharField(
        max_length=Constant.max_length_last_name_user.value,
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]

    def __str__(self) -> str:
        return f'{self.user} подписан на {self.author}'
