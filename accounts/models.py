import pyotp as pyotp
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone


class User(AbstractUser):
    key = models.CharField(max_length=100, unique=True, blank=True)

def generate_key():
    """ User otp key generator """
    key = pyotp.random_base32()
    if is_unique(key):
        return key
    generate_key()


def is_unique(key):
    try:
        User.objects.get(key=key)
    except User.DoesNotExist:
        return True
    return False



@receiver(pre_save, sender=User)
def create_key(sender, instance, **kwargs):
    """This creates the key for users that don't have keys"""
    print("KEY GENERATED")
    if not instance.key:
        instance.key = generate_key()