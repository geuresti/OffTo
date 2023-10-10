from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.urls import reverse

#from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required

from .forms import LogInForm, CreateAccountForm, ProjectForm, TaskForm
from .models import Project, Task

class UserAuthView(View):

    # GET ROUTER
    def get(self, request, page="log_in"):
        print("\nGET PAGE:\n", page)
        if page == "log_in":
            return self.log_in(request)
        if page == "create_account":
            return self.create_account(request)
        elif page == "log_out":
            return self.log_out(request)
        else:
            print("\nREDIRECTING TO LOG IN")
            return redirect("log_in")

    # POST ROUTER
    def post(self, request, page):
        # /Offto/accounts/<log_in/create_account>
        print("\nPOST PAGE:\n", page)
        if page == "log_in":
            return self.log_in_post(request)
        elif page == "create_account":
            return self.create_account_post(request)
        else:
            return redirect("log_in")

    # GET -> "log_in"
    def log_in(self, request):
        if request.user.is_authenticated:
            return redirect("index")
        else:
            form = LogInForm
            context = {
                'log_in_form':form,
            }
            return render(request, 'ProjectManager/log_in.html', context)

    # POST -> "log_in"
    def log_in_post(self, request):
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                # check if account with that username exists
                does_user_exist = User.objects.get(username=username)
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    messages = ['successfully logged in']
                    context = {
                        "messages":messages,
                        "user":user,
                    }
                    request.user = user
                    return redirect("index")  # NOT SURE HOW TO PASS CONTEXT
                else:       # incorrect password
                    messages = ['incorrect password']
                    context = {
                        'log_in_form':form,
                        'messages':messages
                    }
                    return render(request, 'ProjectManager/log_in.html', context)
            except:         # username doesn't exist
                messages = ['an account with that username does not exist']
                context = {
                    'log_in_form':form,
                    'messages':messages
                }
                return render(request, 'ProjectManager/log_in.html', context)
        else:
            # invalid form submitted
            return self.log_in(request)

    # GET -> "log_out"
    def log_out(self, request):
        user = request.user
        if user.username:
            print("\nLEGIT USER DETECTED\n")
            logout(request)

        return redirect("log_in")

    # GET -> "create_account"
    def create_account(self, request, messages=[]):
        form = CreateAccountForm
        context = {
            'create_account_form':form,
            'messages':messages
        }
        return render(request, 'ProjectManager/create_account.html', context)

    # POST -> "create_account"
    def create_account_post(self, request):
        form = CreateAccountForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
#########    User.objects.create_user(username, email, password) ###############

            messages = ['account successfully created']
            context = {'messages':messages}
            return render(request, 'ProjectManager/index.html', context)
        else:
            # invalid form submitted
            messages = ['passwords do not match']
            return self.create_account(request, messages)

# for CRUDing projects
class ProjectManagementView(View):

    # GET ROUTER
    def get(self, request, page, project_id=None):
        print("\nGET PAGE:\n", page)
        if page == "create":
            return self.create_project(request)
        elif page == "edit":
            if project_id:
                print("\nEDITTING PROJECT ID:", project_id, "\n")
                return self.edit_project(request, project_id)
            else:
                print("\nNO PROJECT ID PROVIDED, redirecting to index\n")
                return redirect("index")
        elif page == "view":
            print("\nVIEWING PROJECT ID:", project_id, "\n")
            return self.view_project(request, project_id)
        elif page == "delete":
            print("\nDELETING PROJECT ID:", project_id, "\n")
            return self.delete_project(request, project_id)
        else:
            print("\nREDIRECTING TO INDEX")
            return redirect("index")

    # POST ROUTER
    def post(self, request, page, project_id=None):
        print("\nPOST PAGE:\n", page)
        if page == "create":
            return self.create_project_post(request)
        elif page == "edit":
            return self.edit_project_post(request, project_id)
        else:
            return redirect("log_in")

    # GET -> "create"
    def create_project(self, request):
        form = ProjectForm
        context = {
            'create_project_form':form,
        }
        return render(request, 'ProjectManager/create_project.html', context)

    # POST -> "create"
    def create_project_post(self, request):
        form = ProjectForm(request.POST)

        if form.is_valid():
            if request.user.is_authenticated:
                new_project = Project()

                title = form.cleaned_data['project_title']
                description = form.cleaned_data['project_description']
                deadline = form.cleaned_data['project_deadline']

                new_project.project_owner = request.user
                new_project.project_title = title
                new_project.project_description = description
                new_project.project_deadline = deadline

                new_project.save()
                print("\n NEW PROJECT SUCCESSFULLY CREATED \n")
                return redirect("index")

            else:
                print("\n User trying to create project while not authenticated")
        else:
            print("\n CREATE PROJECT INVALID FORM \n")

        return render(request, 'ProjectManager/index.html')

    # GET -> "edit"
    def edit_project(self, request, project_id):
        if request.user.is_authenticated:
            # prefill form with project information
            project = get_object_or_404(Project, pk=project_id)
            if request.user == project.project_owner:
                form = ProjectForm(instance=project)

                context = {
                    'project':project,
                    'project_form':form
                }

                return render(request, 'ProjectManager/edit_project.html', context)
            else:
                return redirect("index")
        else:
            return redirect("log_in")

    # POST -> "edit"
    def edit_project_post(self, request, project_id):
        form = ProjectForm(request.POST)
        project = get_object_or_404(Project, pk=project_id)

        if form.is_valid():
            if request.user == project.project_owner:
                print("\n VALID EDIT POST REQUEST \n")

                title = form.cleaned_data['project_title']
                description = form.cleaned_data['project_description']
                deadline = form.cleaned_data['project_deadline']

                project.project_title = title
                project.project_description = description
                project.project_deadline = deadline

                project.save()

        return redirect("index")

    # GET -> "view"
    def view_project(self, request, project_id):
        if request.user.is_authenticated:
            project = get_object_or_404(Project, pk=project_id)
            tasks = project.task_set.all()

            context = {
                'project':project,
                'tasks':tasks
            }

            return render(request, 'ProjectManager/view_project.html', context)
        else:
            return redirect("index")

    # GET -> "delete"
    def delete_project(self, request, project_id):
        if request.user.is_authenticated:
            project = get_object_or_404(Project, pk=project_id)
            if project.project_owner == request.user:
                project.delete()
                print("\nPROJECT ID:", project_id, "SUCCESSFULLY DELETED\n")
            else:
                print("\nYou do not have permission to delete this project \n")
            return redirect("index")
        else:
            print("\nLog in first to perform this action \n")
            return redirect("log_in")

# for CRUDing tasks
class TaskManagementView(View):
    def get(self, request, project_id):
        create_task_form = TaskForm
        project = get_object_or_404(Project, pk=project_id)
        context = {
            'create_task_form':create_task_form,
            'project':project
        }
        return render(request, 'ProjectManager/create_task.html', context)

    def post(self, request, project_id):
        form = TaskForm(request.POST)
        project = get_object_or_404(Project, pk=project_id)

        if form.is_valid():
            if request.user.is_authenticated:
                new_task = Task()

                title = form.cleaned_data['task_title']
                description = form.cleaned_data['task_description']
                deadline = form.cleaned_data['deadline']

                new_task.task_title = title
                new_task.task_description = description
                new_task.task_project = project
                #task groups
                #people assigned
                new_task.deadline = deadline

                new_task.save()
                print("\n NEW TASK SUCCESSFULLY CREATED \n")

                url = reverse("view_project", kwargs={'page':'view', 'project_id':project_id})
                return redirect(url)

            else:
                print("\n User trying to create project while not authenticated")
        else:
            print("\n CREATE TASK INVALID FORM \n")


# if requester is not authenticated, redirect them to log in page
def index_view(request):
    if request.user.is_authenticated:
        print("(authed) USER:", request.user, "\n")
        user_projects = request.user.project_set.all()
        context = {
            'user_projects':user_projects
        }
        return render(request, 'ProjectManager/index.html', context)
    else:
        print("redirecting from INDEX to LOG IN", "\n")
        return redirect("log_in")
