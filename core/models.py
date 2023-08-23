from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.urls import reverse
import uuid
# 
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username,  email, password=None):

        if not email:
            raise ValueError('User must have email')
        if not username:
            raise ValueError('User must have username')

        user=self.model(
            email = self.normalize_email(email),
            username= username,
            first_name= first_name,
            last_name= last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email= self.normalize_email(email),
            username= username,
            password= password,
            first_name= first_name,
            last_name=last_name,
        )
        user.is_admin= True
        user.is_active= True
        user.is_staff= True
        user.is_superuser= True
        user.save(using= self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=50)
    username= models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    followers = models.ManyToManyField(
        "self", blank=True, related_name="following", symmetrical=False
    )

    # required fields
    date_joined= models.DateTimeField(default=timezone.now)
    last_login= models.DateTimeField(default=timezone.now)
    modified_date= models.DateTimeField(default=timezone.now)

    objects= UserManager()

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=['username','first_name', 'last_name']

    @property
    def profile(self):
        return self._profile_cache if hasattr(self, '_profile_cache') else self._profile

    @profile.setter
    def profile(self, value):
        if isinstance(value, Profile):
            self._profile_cache = value
            self._profile = None
        else:
            self._profile_cache = None
            self._profile = value

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return self.is_admin 

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True   



class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username= models.CharField(max_length=50, unique=True)
    phone_number= models.CharField(max_length=12, blank=True)
    bio= models.CharField(max_length=200, default='', blank=True)
    location= models.CharField(max_length=100, blank=True)
    profileimg= models.ImageField(upload_to='user/', default='user-default.png')
    
    
    def __str__(self):
        return self.username


    @property
    def imageURL(self):
        try:
            url= self.profileimg.url
        except:
            url = ''
        return url
    
class Post(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    caption = models.TextField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to='post/',)
    likes = models.ManyToManyField(User, related_name='post_likes')

    class Meta:
        ordering= ['-created_at']

    def __str__(self):
        return f"{self.owner} | {self.created_at.strftime('%d/%m/%Y, %H:%M')}"
    
    def get_absolute_url(self):
        return reverse('index')
   
    @property
    def imageURL(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url    
    
    
    @property
    def likesCount(self):
        return self.likes.all().count()
    @property
    def likers(self):
        return self.likes.values_list('id', flat=True)
    

    