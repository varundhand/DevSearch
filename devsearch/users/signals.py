from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User # the default django admin users
from .models import Profile

# @receiver(post_save,sender=Profile) this is second method of using django signals 
def createProfile(sender, instance, created, **kwargs):  #whenever a user is created a profile will be created
  if created: #if its the first instance of the user # CREATED = TRUE
    user = instance # instance is the sender i.e. 'User' 
    profile = Profile.objects.create(
      user= user,
      username = user.username,
      email= user.email,
      name = user.first_name,
    )

def updateUser(sender,instance,created,**kwargs): #whenever user is updated the profile is updated too
  profile = instance 
  user = profile.user
  if created == False: # CREATED = FALSE, so if instance is created first time, it goes to createProfile 
    user.first_name = profile.name
    user.username = profile.username
    user.email = profile.email
    user.save()

def deleteUser(sender,instance, **kwargs):
  user = instance.user #one to one relaionship of user and profile
  user.delete()
  
#connecting a reciever to a sender(reciever is the function 'profileUpdated' and sender is the model which triggers it i.e. 'Profile' )
post_save.connect(createProfile, sender=User)  #anytime user model is created a profile will be created
post_save.connect(updateUser,sender=Profile) # ANYTIME PROFILE IS UPDATED, WE WILL TRIGGER UPDATE-USER WHICH WILL IN TURN UPDATE THE USER
post_delete.connect(deleteUser, sender=Profile) #anytime profile is deleted the user is also deleted (this is made for ADMIN i.e. we already have models.cascade on the user field so if user is deleted , profile is also deleted but for some reason if the admin deletes the profile, the user will NOT GET DELETED, thats why we make a deleteUser signal)
  