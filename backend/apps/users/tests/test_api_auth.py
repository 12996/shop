from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient


class MockTokenAuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="lisi",
            password="Password123!",
            phone="13800000001",
            role="user",
        )

    def test_profile_supports_mock_token_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer mock-token-{self.user.id}")

        response = self.client.get("/api/auth/profile")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["username"], "lisi")
