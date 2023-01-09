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
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form':form}
    return render(request, 'projects/project_form.html',context)

@login_required(login_url='login')
def updateProject(request,pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project) #using instance to pre fill the form fields with project data
    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form':form}
    return render(request, 'projects/project_form.html',context)

@login_required(login_url='login')
def deleteProject(request,pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    context = {'object':project}
    return render(request, 'projects/delete_template.html',context)
