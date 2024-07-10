from django.db import models
from django.contrib.auth.models import AbstractUser

ROLES = (
    ("admin", "Admin"),
    ("user", "User"),
)

PRIORITY_CHOICES = (
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
)

COMPLETE_STATUS = (
    ("todo", "TODO"),
    ("inprogress", "INPROGRESS"),
    ("done", "DONE"),
)


class User(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=5, choices=ROLES, default="user")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username"
    ]  # username is still required but email is used for login


class Task(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(
        max_length=6, choices=PRIORITY_CHOICES, default="medium"
    )
    complete_status = models.CharField(
        max_length=20, choices=COMPLETE_STATUS, default="todo"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_tasks"
    )
    attachment = models.FileField(
        upload_to="task_attachments/", blank=True, null=True
    )  # for file attachments
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User(), on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class TaskList(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    tasks = models.ManyToManyField(Task, related_name="task_lists", blank=True)

    def __str__(self):
        return self.name
