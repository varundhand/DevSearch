from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required #login required decorator 
from django.contrib import messages #flash messages
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import *
from .forms import CustomUserCreationForm,ProfileForm,SkillForm

# Create your views here.
def loginUser(request):
  page = "login"
  if request.user.is_authenticated: #working as a decorator that prevents logged in user to access the login page
    return redirect('profiles')

  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    try: # we want to display the errors if something went wrong
      user = User.objects.get(username=username) #checks whether the user exists in database or not(checks whether the username matches the one in database)
    except:
      messages.error(request,'Username doesnt exist')

    user = authenticate(request,username=username,password=password) #checks whether the username matches the password and will return either 'user instance' or return none

    if user is not None:
      login(request,user) #login function creates a session for this user in the database and adds that in browser's cookies
      return redirect ('profiles')
    else:
      messages.error(request,'Username/Password incorrect')

  context = {'page':page}
  return render(request, 'users/login_register.html', context)

def logoutUser(request):
  logout(request)
  messages.info(request,'User was logged out!')
  return redirect('login')

def registerUser(request):
  page = "register"
  form = CustomUserCreationForm()

  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False) #holding a temporary instance of the form and we are doing this so that we can modify it
      user.username = user.username.lower() #just making sure that the username is lowercase(we dont want them to be case sensative)
      user.save()

      messages.success(request,'User account was created!')

      login(request, user)
      return redirect('edit-account')

    else:
      messages.success(request, 'An error has occurred during registration')
  context= {'page':page, 'form': form }
  return render(request,'users/login_register.html', context)

def profiles(request):
  profiles = Profile.objects.all()
  context = {'profiles':profiles}
  return render(request, 'users/profiles.html',context)

def userProfile(request,pk):
  profile = Profile.objects.get(id=pk)
  topSkills = profile.skill_set.exclude(description__exact='')  # if exclude the 'skills' with description as null
  otherSkills = profile.skill_set.filter(description__exact='') # filter those skills with null description

  context ={'profile':profile,'topSkills':topSkills, 'otherSkills':otherSkills}
  return render(request,'users/user-profile.html',context)

@login_required(login_url='login')
def userAccount(request): #we wont be using a primary key because we can easily iterate the user by 'request.user'
  profile = request.user.profile #its one to one relationship so it can be used as user.profile
  skills = profile.skill_set.all()  
  projects = profile.project_set.all()
  
  context = {'profile':profile, 'skills':skills,'projects':projects}
  return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
  profile = request.user.profile #the logged in user
  form = ProfileForm(instance=profile)

  if request.method == 'POST':
    form = ProfileForm(request.POST, request.FILES, instance=profile) #request.FILES to pass the image of the form
    if form.is_valid():
      form.save()
      return redirect('account')
  context = {'form':form}
  return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
  profile = request.user.profile
  form = SkillForm()

  if request.method == 'POST':
    form = SkillForm(request.POST)
    if form.is_valid():
      skill = form.save(commit=False)
      skill.owner =  profile
      skill.save()
      messages.success(request,'Skill was added successfully!')
      return redirect('account')

  context = {'form':form}
  return render(request, 'users/skill_form.html',context )

@login_required(login_url='login')
def updateSkill(request, pk):
  profile = request.user.profile
  skill = profile.skill_set.get(id=pk)
  form = SkillForm(instance=skill)

  if request.method == 'POST':
    form = SkillForm(request.POST,instance=skill)
    if form.is_valid():
      form.save()
      messages.success(request,'Skill was updated successfully!')
      return redirect('account')
      
  context = {'form':form}
  return render(request, 'users/skill_form.html',context )

def deleteSkill(request,pk):
  profile = request.user.profile
  skill = profile.skill_set.get(id=pk)
  if request.method == 'POST':
        skill.delete()
        messages.success(request,'Skill was deleted successfully!')
        return redirect('account')

  context= {'object':skill}
  return render(request, 'delete_template.html',context)