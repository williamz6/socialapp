from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your models here.
User = get_user_model()

class chatManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset.filter(lookup).distinct()
        return qs

class Chat(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='chat_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='chat_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = chatManager()
    class Meta:
        unique_together =['first_person', 'second_person']

class chatMessage(models.Model):
    chat= models.ForeignKey(Chat, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)