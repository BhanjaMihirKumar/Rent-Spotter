# authentication_app/models.py

from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    image = models.ImageField(upload_to='images', default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo= models.ImageField(upload_to='profile_photos', blank=True, null=True)
    
    extra_photos = models.ManyToManyField(Image, blank=True)
    bio = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,blank=True,decimal_places=0, default=0)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    bedroom = models.DecimalField( max_digits=5, decimal_places=0, blank=True, default=0)
    hallroom = models.DecimalField( max_digits=5, decimal_places=0, blank=True, default=0)
    kitchen = models.DecimalField( max_digits=5, decimal_places=0, blank=True, default=0)
    location_info = models.CharField(max_length=100, blank=True )
    location_2 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username
