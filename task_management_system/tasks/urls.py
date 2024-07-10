from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    PasswordResetView,
    TaskListView,
    TaskCreateView,
    TaskDetailView,
    CommentListCreateView,
    TaskListListCreateView,
    TaskListDetailView,
    UserListView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("user-list", UserListView.as_view(), name="user-list"),
    path("password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("tasks", TaskListView.as_view(), name="task_list"),
    path("tasks/", TaskCreateView.as_view(), name="task_create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path(
        "tasks/<int:task_id>/comments/",
        CommentListCreateView.as_view(),
        name="comment_list_create",
    ),
    path("tasklists/", TaskListListCreateView.as_view(), name="tasklist_list_create"),
    path("tasklists/<int:pk>/", TaskListDetailView.as_view(), name="tasklist_detail"),
]
