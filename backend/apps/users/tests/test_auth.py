from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTest(TestCase):
    def test_create_user_with_role(self):
        user = get_user_model().objects.create_user(
            username="zhangsan",
            password="123456",
            phone="13800000000",
            role="user",
        )

        self.assertEqual(user.username, "zhangsan")
        self.assertEqual(user.role, "user")
