from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_provider = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    total_ratings = models.IntegerField(default=0)
    activation_token = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {'Proveedor' if self.is_provider else 'Cliente'}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
