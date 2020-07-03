from django.test import TestCase
from ..models import generate_recipe_image_path
from unittest.mock import patch


class ModelTests(TestCase):
    "recipe app models test."

    @patch('uuid.uuid4')
    def test_image_upload_correct_path(self, mock_uuid):
        uuid = "test"
        mock_uuid.return_value = uuid
        file_path = generate_recipe_image_path(
            None, "my_image.jpg")
        expected_path = f"uploads/recipe/{uuid}.jpg"
        self.assertEqual(file_path, expected_path)
