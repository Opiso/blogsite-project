# # signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Author

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile when the user is created or updated.
    """
    # if created:
    #     # Create a new profile for the new user
    #     Author.objects.create(user=instance)
    # else:
    #     # Check if the user profile exists before updating it
    #     if hasattr(instance, 'author'):
    #         instance.author.save()
    #     else:
    #         # Create the user profile if it doesn't exist
    #         Author.objects.create(user=instance)

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'author'):
        Author.objects.create(user=instance)
        instance.author.save()