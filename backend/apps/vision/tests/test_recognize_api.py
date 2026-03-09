from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient


class RecognizeApiTest(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.merchant = get_user_model().objects.create_user(
            username="vision_merchant",
            password="12345678",
            phone="13500000000",
            role="merchant",
        )

    def test_recognize_returns_candidate_fields(self):
        self.api_client.force_authenticate(user=self.merchant)
        image_file = SimpleUploadedFile(
            "sample.jpg",
            b"fake-image-content",
            content_type="image/jpeg",
        )

        response = self.api_client.post(
            "/api/admin/vision/recognize",
            {"image": image_file},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("recognized_name", response.data)
        self.assertIn("recommended_category_id", response.data)
        self.assertIn("recommended_category_name", response.data)
        self.assertIn("confidence", response.data)
