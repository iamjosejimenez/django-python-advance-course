"""
Test for models.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTest(TestCase):
    """Test model."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with email is successful."""

        email = "test@example.com"
        password = "testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_is_normalized(self):
        """Test email is normalized for new users."""

        sample_emails = [
            ("test1@EXAMPLE.com", "test1@example.com"),
            ("test2@Example.com", "test2@example.com"),
            ("test3@example.COM", "test3@example.com"),
            ("TEST4@EXAMPLE.COM", "TEST4@example.com"),
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        """Test superuser creation is successful"""
        user = get_user_model().objects.create_superuser(
            "superuser@admin.com",
            "superuser123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
