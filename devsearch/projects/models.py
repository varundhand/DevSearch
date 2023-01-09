from django.db import models
import uuid
from users.models import Profile

# Create your models here.
# creating classes that represent tables of our database

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True,blank=True,on_delete=models.SET_NULL) # IMPORTANT! WE IMPORTED THE USER-MODELS IN PROJECT-MODELS AND USER THE PROFILE MODEL AS PARENT MODEL
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank= True) #this is not a comulsory field for input of data
    featured_image = models.ImageField(null=True, blank= True, default='default.jpg')
    demo_link = models.CharField(max_length=2000,null=True, blank= True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag',blank=True)  #we put quotes on Tag model because its situated below Project model 
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True) # 'created' and 'id' will be taken in every model class
    id = models.UUIDField(default=uuid.uuid4,unique=True, editable=False, primary_key=True) #we overrid the id with our new uuid primary key
    # univeral unique identifier is used as primary key here 

    def __str__(self):
        return self.title

class Review(models.Model):
    # making a drop down menu to choose from
    VOTE_TYPE=(
        ('up', 'UP VOTE'),
        ('down', 'DOWN VOTE'),
    )
    # owner=
    project= models.ForeignKey(Project, on_delete=models.CASCADE)  # models.cascade --> deletes the reviews on deletion of project & models.SET_NULL --> reviews remain on deletion fo the project 
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, editable=False, primary_key=True) 
    
    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, editable=False, primary_key=True)

    def __str__(self):
        return self.name


        