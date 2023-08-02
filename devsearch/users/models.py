from django.db import models
from django.contrib.auth.models import User # the default django admin users
import uuid
# Create your models here.

from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) #models.cascade ensures that on deletion of user, the profile is also deleted
  name = models.CharField(max_length=200,blank=True,null=True)
  email = models.EmailField(max_length=500,blank=True, null=True)
  username = models.CharField(max_length=200,blank=True,null=True)
  location = models.CharField(max_length=200,blank=True,null=True)
  short_intro = models.CharField(max_length=200,blank=True,null=True)
  bio = models.TextField(blank=True,null=True)
  profile_image = models.ImageField(null=True,blank=True,upload_to='profiles/',default='profiles/user-default.png') #profiles in static folder within images 
  social_github = models.CharField(max_length=200, blank=True, null=True)
  social_twitter = models.CharField(max_length=200, blank=True, null=True)
  social_linkedin = models.CharField(max_length=200, blank=True, null=True)
  social_youtube = models.CharField(max_length=200, blank=True, null=True)
  social_website = models.CharField(max_length=200, blank=True, null=True)
  created = models.DateTimeField(auto_now_add=True)
  id = models.UUIDField(default=uuid.uuid4,unique=True, editable=False, primary_key=True) 
    
  def __str__(self):
    return str(self.username) #the user name should we converted into string because integers may be used in them

class Skill(models.Model):
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True,blank=True)
  name = models.CharField(max_length=200,blank=True,null=True)
  description = models.TextField(blank=True,null=True)
  created = models.DateTimeField(auto_now_add=True)
  id = models.UUIDField(default=uuid.uuid4,unique=True, editable=False, primary_key=True) 
   
  def __str__(self):
    return str(self.name)
  
  # class Meta: # META DATA provides information about other data. so here meta tags can be used to provide information about the django model 
