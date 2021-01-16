from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse


class Chief(models.Model):
    '''
    Модель отзывов от посетителей
    '''
    POSITIONS = (
        ('Генеральный директор', 'Генеральный директор'),
        ('Шеф повар', 'Шеф повар'),
        ('Повар', 'Повар'),
        ('Стажер', 'Стажер'),
    )

    EDUCATIONS = (
        ('Бакалавр', 'Бакалавр'),
        ('Колледж или техникум', 'Колледж или техникум'),
        ('Самоучка', 'Самоучка'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    position = models.CharField(
        verbose_name='Должность',
        choices=POSITIONS,
        default=POSITIONS[0][0],
        max_length=200
    )

    education = models.CharField(
        verbose_name='Образование',
        choices=EDUCATIONS,
        default=EDUCATIONS[0][0],
        max_length=200
    )

    work_experience = models.FloatField(
        verbose_name='Реальный стаж работы'
    )

    work_history = models.CharField(
        verbose_name='История работы',
        max_length=200
    )


    def get_absolute_url(self):
        return reverse('teams:teams')

    def __str__(self):
        return f'{self.user} {self.position}'