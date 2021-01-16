from django.contrib.auth.models import User
from .models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(signal=post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''Функция создает профиль пользователя при создании пользователя'''
    if created:
        UserProfile.objects.create(user=instance) 


@receiver(signal=post_save, sender=User)
def assign_profile(sender, instance, **kwargs):
    '''Данная функция присваивает профиль к пользователю'''
    instance.userprofile.save()        