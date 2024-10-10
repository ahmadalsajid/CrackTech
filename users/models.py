from django.contrib.auth.hashers import identify_hasher
from django.db import models
from enum import Enum
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    phone = models.CharField(max_length=50, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username}::{self.get_full_name()}'

    class Meta:
        ordering = ('-created_at',)



class Student(models.Model):
    user = models.OneToOneField(User, related_name='student', on_delete=models.CASCADE)
    registration = models.CharField(max_length=8)
    name = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.registration}: {self.user.get_full_name()}'

    class Meta:
        ordering = ('-created_at',)


@receiver(post_save, sender=User)
def set_user_pass(sender, instance, **kwargs):
    try:
        hasher = identify_hasher(instance.password)
    except Exception as e:
        instance.set_password(instance.password)
        instance.save()
