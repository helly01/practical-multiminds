from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, filters, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    UserSerializer,
    TaskSerializer,
    CommentSerializer,
    TaskListSerializer,
)
from .models import User, Task, Comment, TaskList
from .permissions import IsAdminUser
from .utils import send_welcome_email


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        send_welcome_email(user)


# Handle login and generate token
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Please provide both email and password."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response(
                {"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        user.set_password(request.data["password"])
        user.save()
        return Response(status=204)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]


class TaskListView(generics.ListAPIView):
    """
    get:
    Return a list of all tasks created by the authenticated user.

    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["priority", "complete_status"]  # Add fields for filtering
    search_fields = ["title", "created_by__username"]  # Fields to search

    # def get_queryset(self):
    #     return Task.objects.filter(created_by=self.request.user)
    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user) | Task.objects.filter(
            assigned_to=self.request.user
        )

    # use to save any instance without any validation
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Return the details of a task.

    patch:
    Partially update a task.

    delete:
    Delete a task.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user) | Task.objects.filter(
            assigned_to=self.request.user
        )


class CommentListCreateView(generics.ListCreateAPIView):
    """
    get:
    Return a list of comments for a task.

    post:
    Create a new comment on a task.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs["task_id"]
        return Comment.objects.filter(task_id=task_id)

    def perform_create(self, serializer):
        task_id = self.kwargs.get("task_id")  # Get the task_id from URL
        task = Task.objects.get(id=task_id)
        serializer.save(
            task=task, author=self.request.user
        )  # Associate the task and author


class TaskListListCreateView(generics.ListCreateAPIView):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["is_public"]  # Add fields for filtering
    search_fields = ["name", "owner__username"]  # Fields to search

    def get_queryset(self):
        return TaskList.objects.filter(
            owner=self.request.user
        ) | TaskList.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskListDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskList.objects.filter(
            owner=self.request.user
        ) | TaskList.objects.filter(is_public=True)
