from django.test import SimpleTestCase
from django.urls import reverse, resolve
from reservations.views import *


class TestUrls(SimpleTestCase):

    def test_calendar_url_resolves(self):
        url = reverse('calendar')
        self.assertEqual(resolve(url).func.view_class, CalendarReservation)

    def test_requests_url_resolves(self):
        url = reverse('requests')
        self.assertEqual(resolve(url).func.view_class, ListReservation)

    def test_request_user_cancel_url_resolves(self):
        url = reverse('request_user_cancel')
        self.assertEqual(resolve(url).func.view_class, ListReservation)

    def test_requests_pending_url_resolves(self):
        url = reverse('requests_pending')
        self.assertEqual(resolve(url).func.view_class, ListReservationPending)

    def test_manage_solicitation_url_resolves(self):
        url = reverse('manage_solicitation', kwargs={'id': 1})
        self.assertEqual(resolve(url).func.view_class, ManageSolicitationView)

    def test_calendar_manager_url_resolves(self):
        url = reverse('calendar_manager')
        self.assertEqual(resolve(url).func.view_class, CalendarManagerReservation)

    def test_request_dashboard_url_resolves(self):
        url = reverse('request_dashboard')
        self.assertEqual(resolve(url).func.view_class, DashboardRequestPageView)

    def test_total_request_url_resolves(self):
        url = reverse('total_request')
        self.assertEqual(resolve(url).func.view_class, ListReservationManager)

    def test_request_cancel_url_resolves(self):
        url = reverse('request_cancel')
        self.assertEqual(resolve(url).func.view_class, ListReservationManager)

    def test_all_hours_url_resolves(self):
        url = reverse('all_hours')
        self.assertEqual(resolve(url).func.view_class, HourListView)

    def test_create_hours_url_resolves(self):
        url = reverse('create_hours')
        self.assertEqual(resolve(url).func.view_class, HourCreateView)

    def test_edit_hours_url_resolves(self):
        url = reverse('edit_hours', kwargs={'hours_id': 1})
        self.assertEqual(resolve(url).func.view_class, HourUpdateView)

    def test_delete_hours_url_resolves(self):
        url = reverse('delete_hours', kwargs={'hours_id': 1})
        self.assertEqual(resolve(url).func.view_class, HourDeleteView)





