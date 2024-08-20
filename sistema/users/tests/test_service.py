from django.test import TestCase
from users.models import User
from users.service import UserService

class UserServiceTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password', email="user1@example.com", first_name="John", user_type="teacher")
        self.user2 = User.objects.create_user(username='user2', password='password', email="user2@example.com", first_name="Jane", user_type="manager")

    def test_list_all_users(self):
        users = UserService.list_all_users(page=1, per_page=1)
        self.assertEqual(users.paginator.count, 2)
        self.assertEqual(users.number, 1)

    def test_get_user_details(self):
        user = UserService.get_user_details(self.user1.id)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "user1@example.com")

        user_none = UserService.get_user_details(999)  # ID que não existe
        self.assertIsNone(user_none)

    def test_create_new_user(self):
        new_user = UserService.create_new_user(first_name="Jim", email="jim@example.com", password="password", user_type="teacher")
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(new_user.email, "jim@example.com")
        self.assertEqual(new_user.username, "jim")
        self.assertTrue(new_user.check_password("password"))

    def test_update_existing_user(self):
        updated_user = UserService.update_existing_user(self.user1.id, first_name="John Updated")
        self.user1.refresh_from_db()
        self.assertEqual(updated_user.first_name, "John Updated")
        self.assertEqual(self.user1.first_name, "John Updated")

    def test_delete_user(self):
        success = UserService.delete_user(self.user1.id)
        self.assertTrue(success)
        self.assertEqual(User.objects.count(), 1)
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())

    def test_search_users(self):
        # Teste de busca pelo nome
        results_by_name = UserService.search_users("John", page=1, per_page=10)
        self.assertEqual(results_by_name.paginator.count, 1)
        self.assertIn(self.user1, results_by_name)
        
        # Teste de busca pelo email
        results_by_email = UserService.search_users("user2@example.com", page=1, per_page=10)
        self.assertEqual(results_by_email.paginator.count, 1)
        self.assertIn(self.user2, results_by_email)

        # Teste de busca por um nome que não existe
        results_none = UserService.search_users("NoName", page=1, per_page=10)
        self.assertEqual(results_none.paginator.count, 0)