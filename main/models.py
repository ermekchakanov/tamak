from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse


class UserProfile(models.Model):
    '''
    Модель профиля пользователя
    '''
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    user_photo = models.ImageField(
        upload_to='user_profiles'
    )

    def __str__(self):
        return self.user.username + ' Profile' 

class Feedback(models.Model):
    '''
    Модель отзывов от посетителей
    '''
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва'
    )

    feedback_text = models.TextField(
        verbose_name='Поле для отзыва',
        max_length=200
    )

    date_created = models.DateTimeField(
        verbose_name='Дата и время отзыва',
        default=timezone.now
    )

    def get_absolute_url(self):
        return reverse('feedback-details', kwargs={'pk':self.pk})

    def __str__(self):
        return f'{self.author.first_name} {self.author.last_name}'

class Comment(models.Model):
    '''
    Модель комментариев к отзывам
    '''
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )

    assigned_to_feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='comments'
    )

    comment_text = models.TextField(
        verbose_name='Поле для комментария',
        max_length=200
    )

    time = models.DateTimeField(
        verbose_name='Дата и время комментария',
        default=timezone.now
    )

    def __str__(self):
       return f'{self.author.first_name} {self.author.last_name}'


    


