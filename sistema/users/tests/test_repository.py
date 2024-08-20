from django.test import TestCase
from users.models import User
from users.repository import UserRepository

class UserRepositoryTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password', email="user1@example.com", first_name="John", user_type="teacher")
        self.user2 = User.objects.create_user(username='user2', password='password', email="user2@example.com", first_name="Jane", user_type="manager")

    def test_get_all_users(self):
        users = UserRepository.get_all_users()
        self.assertEqual(users.count(), 2)
        self.assertIn(self.user1, users)
        self.assertIn(self.user2, users)

    def test_get_user_by_id(self):
        user = UserRepository.get_user_by_id(self.user1.id)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "user1@example.com")

        user_none = UserRepository.get_user_by_id(999)  # ID que não existe
        self.assertIsNone(user_none)

    def test_get_users_by_type(self):
        teachers = UserRepository.get_users_by_type('teacher')
        managers = UserRepository.get_users_by_type('manager')

        self.assertEqual(teachers.count(), 1)
        self.assertEqual(managers.count(), 1)

        self.assertIn(self.user1, teachers)
        self.assertIn(self.user2, managers)

    def test_create_user(self):
        new_user = UserRepository.create_user(username='user3', password='password', email="user3@example.com", first_name="Jim", user_type="teacher")
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(new_user.email, "user3@example.com")
        self.assertEqual(new_user.user_type, "teacher")

    def test_update_user(self):
        updated_user = UserRepository.update_user(self.user1.id, first_name="John Updated")
        self.user1.refresh_from_db()
        self.assertEqual(updated_user.first_name, "John Updated")
        self.assertEqual(self.user1.first_name, "John Updated")

    def test_delete_user(self):
        success = UserRepository.delete_user(self.user1.id)
        self.assertTrue(success)
        self.assertEqual(User.objects.count(), 1)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

    def test_search_users(self):
        results = UserRepository.search_users("John")
        self.assertEqual(results.count(), 1)
        self.assertIn(self.user1, results)

        results_by_email = UserRepository.search_users("user2@example.com")
        self.assertEqual(results_by_email.count(), 1)
        self.assertIn(self.user2, results_by_email)