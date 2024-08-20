from django.test import TestCase
from users.forms import EmailLoginForm, UserForm, ProfileForm
from users.models import User

class FormsTest(TestCase):

    def test_email_login_form_valid_data(self):
        form = EmailLoginForm(data={
            'email': 'user@example.com',
            'password': 'password123'
        })
        self.assertTrue(form.is_valid())

    def test_email_login_form_invalid_data(self):
        form = EmailLoginForm(data={
            'email': 'invalidemail',  # Invalid email format
            'password': 'password123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_user_form_valid_data(self):
        form = UserForm(data={
            'first_name': 'Test User',
            'email': 'user@example.com',
            'user_type': 'teacher',
            'password': 'password123'
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'test_user')
        self.assertTrue(user.check_password('password123'))

    def test_user_form_invalid_data(self):
        form = UserForm(data={
            'email': '',
            'user_type': '',
            'password': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('user_type', form.errors)
        self.assertIn('password', form.errors)

    def test_user_form_save(self):
        form = UserForm(data={
            'first_name': 'Test User',
            'email': 'user@example.com',
            'user_type': 'teacher',
            'password': 'password123'
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'test_user')
        self.assertTrue(user.check_password('password123'))

    def test_profile_form_valid_data(self):
        user = User.objects.create_user(
            username='testuser',
            first_name='Test User',
            email='user@example.com',
            password='old_password'
        )
        form = ProfileForm(instance=user, data={
            'first_name': 'Updated User',
            'email': 'updated@example.com',
            'password': 'new_password'
        })
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.first_name, 'Updated User')
        self.assertEqual(updated_user.email, 'updated@example.com')
        self.assertTrue(updated_user.check_password('new_password'))

    def test_profile_form_empty_password(self):
        form_data = {
            'first_name': 'UpdatedUser',
            'email': 'updateduser@example.com',
            'password': ''
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)