from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reservations.views import *
from users.views import (
    CustomLoginView, DashboardManagerPage, DashboardTeacherPage,
    UserListView, UserCreateView, UserUpdateView, UserDeleteView, UserProfileView
)
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


class UserUrlsTest(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_manager_dashboard_url_resolves(self):
        url = reverse('manager_dashboard')
        self.assertEqual(resolve(url).func.view_class, DashboardManagerPage)

    def test_teacher_dashboard_url_resolves(self):
        url = reverse('teacher_dashboard')
        self.assertEqual(resolve(url).func.view_class, DashboardTeacherPage)

    def test_user_list_url_resolves(self):
        url = reverse('user_list')
        self.assertEqual(resolve(url).func.view_class, UserListView)

    def test_user_add_url_resolves(self):
        url = reverse('user_add')
        self.assertEqual(resolve(url).func.view_class, UserCreateView)

    def test_user_edit_url_resolves(self):
        url = reverse('user_edit', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, UserUpdateView)

    def test_user_delete_url_resolves(self):
        url = reverse('user_delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, UserDeleteView)

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func.view_class, UserProfileView)

    def test_password_reset_url_resolves(self):
        url = reverse('password_reset')
        self.assertEqual(resolve(url).func.view_class, PasswordResetView)

    def test_password_reset_done_url_resolves(self):
        url = reverse('password_reset_done')
        self.assertEqual(resolve(url).func.view_class, PasswordResetDoneView)

    def test_password_reset_confirm_url_resolves(self):
        url = reverse('password_reset_confirm', kwargs={'uidb64': 'test', 'token': 'test-token'})
        self.assertEqual(resolve(url).func.view_class, PasswordResetConfirmView)

    def test_password_reset_complete_url_resolves(self):
        url = reverse('password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, PasswordResetCompleteView)