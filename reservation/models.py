from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse


class Order (models.Model):
    '''
    Класс для бронирования
    '''
    PERSONS = (
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5),
        ('6', 6),        
    )

    reservator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    phone = models.IntegerField(
        verbose_name='Номер телефона'
    )

    date = models.DateField(
        verbose_name='Дата броинирования'
    )

    time = models.TimeField(
        verbose_name='Время бронирования'
    ) 

    persons = models.CharField(
        verbose_name = 'Количество человек',
        choices=PERSONS,
        default=PERSONS[0][1],
        max_length=200 
    )

    message = models.TextField(
        verbose_name='Комментарии к заказу',
        max_length=200,
        blank=True,
        default='Комментария нет'
    )

    date_created = models.DateTimeField(
        verbose_name='Дата создания заказа',
        default=timezone.now
    )

    def get_absolute_url(self):
        return reverse('reservation:my_reservations')

    def __str__(self):
        '''Описание объекта Order'''
        return f'{self.reservator} {self.date} {self.time}'