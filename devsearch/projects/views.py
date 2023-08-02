#django views are python functions that takes http requests and returns http response in form of html documents
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ProjectForm

def projects(request):
    projects = Project.objects.all()

    context = {'projects': projects}

    return render(request, 'projects/projects.html', context)

def project(request,pk):
    project = Project.objects.get(id=pk)
    # tags = project.tags.all()      WHEN WE NEED TO RENDER MULTIPLE VALUES WE USE FOR LOOP TO RENDER 
    context = {'project':project}
    return render(request, 'projects/single-projects.html',context)

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False) # gives an instance of the project which we can use to iterate it 
            project.owner = profile #SETTING THE OWNER OF THE PROJECT  # the owner of the project is the logged in user i.e. 'profile' 
            project.save()
            return redirect('account')
    context = {'form':form}
    return render(request, 'projects/project_form.html',context)

@login_required(login_url='login')
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk) # we will query only the LOGGED IN USER's projects so that another logged in used is not able to edit other's projects
    form = ProjectForm(instance=project) #using instance to pre fill the form fields with project data
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request, 'projects/project_form.html',context)

@login_required(login_url='login')
def deleteProject(request,pk):
    profile = request.user.profile #    QUERYING LOGGED IN USER'S PROJECTS ONLY so that only the OWNER OF PROJECT could delete it
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    context = {'object':project}
    return render(request, 'delete_template.html',context)


