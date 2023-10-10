from django.urls import path
from ProjectManager.views import *

# /Offto/accounts/<log_in/create_account>

urlpatterns = [
    path('', index_view, name="blank"),
    path('index/', index_view, name="index"),
    path('accounts/<slug:page>/', UserAuthView.as_view(), name="accounts"),
    path('accounts/log_in/', UserAuthView.as_view(), name="log_in"),
    path('projects/<slug:page>/', ProjectManagementView.as_view(), name="projects"),
    path('projects/<slug:page>/<int:project_id>/', ProjectManagementView.as_view(), name="edit_project"),
    path('projects/<slug:page>/<int:project_id>/', ProjectManagementView.as_view(), name="delete_project"),
    path('projects/<slug:page>/<int:project_id>/', ProjectManagementView.as_view(), name="view_project"),
    path('projects/<int:project_id>/tasks/create/', TaskManagementView.as_view(), name="create_task"),
]


# project/edit/PROJECT_ID (get/post)
    # make sure project belongs to user before editting
# project/create (get/post)
    # make sure user does not already have a project with this project_title
