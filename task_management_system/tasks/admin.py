from django.contrib import admin

from .models import User, Task, Comment, TaskList


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "phone_number", "role")
    list_filter = ("role",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "priority",
        "complete_status",
        "assigned_to",
        "created_by",
    )
    list_filter = ("priority", "complete_status", "assigned_to", "created_by")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "author", "content")
    list_filter = ("task", "author")


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "is_public")
    list_filter = ("owner",)
