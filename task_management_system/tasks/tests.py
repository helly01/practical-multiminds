from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User, Task, Comment, TaskList


class UserAuthenticationTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )
        self.client.login(email="test@example.com", password="testpass123")

    def get_login_token(self):
        User = get_user_model()
        if not User.objects.filter(username="testuser").exists():
            User.objects.create_user(
                username="testuser", email="test@example.com", password="testpass123"
            )
        url = reverse("login")
        data = {"email": "test@example.com", "password": "testpass123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        return response.data["token"]

    def test_user_login(self):
        token = self.get_login_token()
        self.assertIsNotNone(token)

    def test_password_reset(self):
        # Obtain the authentication token using the refactored login method
        token = self.get_login_token()

        # Set the token in the client headers
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)

        # Perform the password reset
        url = reverse("password_reset")
        data = {"password": "newpass123"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the password was changed
        user = get_user_model().objects.get(username="testuser")
        user.refresh_from_db()
        self.assertTrue(user.check_password("newpass123"))

    def test_create_task(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        url = reverse("task_create")
        data = {"title": "Test Task", "description": "Test Description"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_task_list(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        Task.objects.create(title="Test Task", created_by=self.user)
        url = reverse("task_list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_task(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        task = Task.objects.create(title="Test Task", created_by=self.user)
        url = reverse("task_detail", kwargs={"pk": task.id})
        data = {"title": "Updated Task"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "Updated Task")

    def test_delete_task(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        task = Task.objects.create(title="Test Task", created_by=self.user)
        url = reverse("task_detail", kwargs={"pk": task.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_comment(self):
        token = self.get_login_token()
        task = Task.objects.create(title="Test Task", created_by=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        url = reverse("comment_list_create", kwargs={"task_id": task.id})
        data = {"text": "Test Comment"}
        response = self.client.post(url, data, format="json")
        print(response.data)  # Add this line to print the response content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_comments(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        task = Task.objects.create(title="Test Task", created_by=self.user)
        Comment.objects.create(task=task, author=self.user, text="Test Comment")
        url = reverse("comment_list_create", kwargs={"task_id": task.id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task_list(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        url = reverse("tasklist_list_create")
        data = {"name": "Test List", "is_public": True}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_task_lists(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        TaskList.objects.create(name="Test List", owner=self.user, is_public=True)
        url = reverse("tasklist_list_create")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_task_list(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        task_list = TaskList.objects.create(name="Test List", owner=self.user)
        url = reverse("tasklist_detail", kwargs={"pk": task_list.id})
        data = {"name": "Updated List"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_list.refresh_from_db()
        self.assertEqual(task_list.name, "Updated List")

    def test_delete_task_list(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        task_list = TaskList.objects.create(name="Test List", owner=self.user)
        url = reverse("tasklist_detail", kwargs={"pk": task_list.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_search_task_by_title(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        url = reverse("task_list") + "?search=Test Task 1"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_task_by_priority(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        url = reverse("task_list") + "?priority=high"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_task_by_completion_status(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        url = reverse("task_list") + "?complete_status=todo"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_task_lists_by_name(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        TaskList.objects.create(name="Test List", owner=self.user, is_public=True)
        url = reverse("tasklist_list_create") + "?search=Test List"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_task_lists_by_public_status(self):
        token = self.get_login_token()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)
        TaskList.objects.create(name="Test List", owner=self.user, is_public=True)
        url = reverse("tasklist_list_create") + "?is_public=True"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
