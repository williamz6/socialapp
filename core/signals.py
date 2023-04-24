from .models import Profile
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save,post_delete
User = get_user_model()

def createProfile(sender, instance, created, **kwargs):
    if created:
        user= instance
        profile = Profile.objects.create(
            user=user,
            username = user.username

        )
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.username= profile.username
        user.save()
post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)