from django.test import TestCase, Client
from django.urls import reverse
from reservations.models import Reservation, Hour
from rooms.models import Room
from users.models import User

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='teacher', password='password', email="teacher@gmail.com")
        self.manager = User.objects.create_user(username='manager', password='password', email="manager@gmail.com")
        self.room = Room.objects.create(name='Sala 1')
        self.hour = Hour.objects.create(range_hour='10:00 - 11:00')
        self.reservation = Reservation.objects.create(
            room=self.room,
            teacher=self.teacher,
            hour=self.hour,
            date='2024-08-20',
            status='pending'
        )

        # Definindo as URLs a serem usadas nos testes
        self.calendar_url = reverse('calendar')
        self.calendar_manager_url = reverse('calendar_manager')
        self.requests_url = reverse('requests')
        self.requests_pending_url = reverse('requests_pending')
        self.manage_solicitation_url = reverse('manage_solicitation', kwargs={'id': self.reservation.id})

    def test_calendar_reservation_get(self):
        self.client.login(email= "teacher@gmail.com", password='password')
        response = self.client.get(self.calendar_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/calendar_teacher.html')
        self.assertContains(response, 'Sala 1')

    def test_calendar_reservation_post(self):
        self.client.login(email= "teacher@gmail.com", password='password')
        data = {
            'room': self.room.id,
            'hours': [self.hour.range_hour],
            'date': '20/08/2024'
        }
        response = self.client.post(self.calendar_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.calendar_url)
        self.assertEqual(Reservation.objects.count(), 2)  # Já existe uma reserva criada no setUp

    def test_list_reservation_get(self):
        self.client.login(email= "teacher@gmail.com", password='password')
        response = self.client.get(self.requests_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/request_teacher.html')
        self.assertContains(response, self.room.name)

    def test_list_reservation_post_cancel(self):
        self.client.login(email= "teacher@gmail.com", password='password')
        response = self.client.post(self.requests_url, {'reservation_id': self.reservation.id})
        self.assertRedirects(response, self.requests_url)
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())

    def test_list_reservation_pending_get(self):
        self.client.login(email= "manager@gmail.com", password='password')
        response = self.client.get(self.requests_pending_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/request_pending.html')

    def test_manage_solicitation_view_post_approve(self):
        self.client.login(email= "manager@gmail.com", password='password')
        response = self.client.post(self.manage_solicitation_url, {'action': 'approved'})
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'approved')
        self.assertRedirects(response, self.requests_pending_url)

    def test_manage_solicitation_view_post_reject(self):
        self.client.login(email= "manager@gmail.com", password='password')
        response = self.client.post(self.manage_solicitation_url, {'action': 'rejected'})
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, 'rejected')
        self.assertRedirects(response, self.requests_pending_url)

    def test_calendar_manager_reservation_get(self):
        self.client.login(email= "manager@gmail.com", password='password')
        response = self.client.get(self.calendar_manager_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations/calendar_manager.html')

    def test_calendar_manager_reservation_post(self):
        self.client.login(email= "manager@gmail.com", password='password')
        data = {
            'room': self.room.id,
            'hours': [self.hour.range_hour],
            'date': '20/08/2024',
            'teacher': self.teacher.id
        }
        response = self.client.post(self.calendar_manager_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.calendar_manager_url)
        self.assertEqual(Reservation.objects.count(), 2)  # Já existe uma reserva criada no setUp