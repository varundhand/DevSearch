# customizing the UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill

#for login and regitser page
class CustomUserCreationForm(UserCreationForm): 
  class Meta:
    model = User
    fields = ['first_name','email','username', 'password1', 'password2'] #from signals.py 
    labels = {
      'first_name':'Name'
      }
  def __init__(self, *args, **kwargs): # FOR STYLING
    super(CustomUserCreationForm,self).__init__(*args,**kwargs)
    for name,field in self.fields.items():
      field.widget.attrs.update({'class':'input'})


class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = ['name','email','username','location','bio','short_intro','profile_image','social_github','social_linkedin','social_twitter','social_youtube','social_website'] #could have used exclude instaed of this long syntax
  def __init__(self, *args, **kwargs): # FOR STYLING
    super(ProfileForm,self).__init__(*args,**kwargs)
    for name,field in self.fields.items():
      field.widget.attrs.update({'class':'input'})  


class SkillForm(ModelForm):
  class Meta:
    model = Skill
    fields = '__all__'
    exclude = ['owner']
  def __init__(self, *args, **kwargs): # FOR STYLING
    super(SkillForm,self).__init__(*args,**kwargs)
    for name,field in self.fields.items():
      field.widget.attrs.update({'class':'input'})  