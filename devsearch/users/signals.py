from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User # the default django admin users
from .models import Profile

# @receiver(post_save,sender=Profile) this is second method of using django signals 
def createProfile(sender, instance, created, **kwargs):  #whenever a user is created a profile will be created
  if created: #if its the first instance of the user
    user = instance # instance is the sender i.e. 'User' 
    profile = Profile.objects.create(
      user= user,
      username = user.username,
      email= user.email,
      name = user.first_name,
    )

def deleteUser(sender,instance, **kwargs):
  user = instance.user
  user.delete()
  
#connecting a reciever to a sender(reciever is the function 'profileUpdated' and sender is the model which triggers it i.e. 'Profile' )
post_save.connect(createProfile, sender=User) 
post_delete.connect(deleteUser, sender=Profile)
  