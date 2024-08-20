from django.test import TestCase
from users.models import User
from rooms.models import Room
from reservations.models import Hour, Reservation, ReservationApproval
from datetime import datetime

class ReservationModelTest(TestCase):

    def setUp(self):
        # Cria instâncias para usar nos testes
        self.teacher = User.objects.create_user(username='teacher', password='password', email="teacher@example.com", first_name="John", user_type="teacher")
        self.manager = User.objects.create_user(username='manager', password='password', email="manager@example.com", first_name="Jane", user_type="manager")
        self.room = Room.objects.create(name="Sala 1")
        self.hour = Hour.objects.create(range_hour="10:00 - 11:00")
        self.reservation = Reservation.objects.create(
            room=self.room,
            teacher=self.teacher,
            hour=self.hour,
            date=datetime.strptime('2024-08-20', '%Y-%m-%d').date(),
            status='pending'
        )

    def test_hour_creation(self):
        # Testa se a criação do Hour foi bem-sucedida
        self.assertEqual(self.hour.range_hour, "10:00 - 11:00")
        self.assertEqual(str(self.hour), "10:00 - 11:00")

    def test_reservation_creation(self):
        # Testa se a criação da Reservation foi bem-sucedida
        self.assertEqual(self.reservation.room, self.room)
        self.assertEqual(self.reservation.teacher, self.teacher)
        self.assertEqual(self.reservation.hour, self.hour)
        self.assertEqual(self.reservation.date.strftime('%Y-%m-%d'), '2024-08-20')
        self.assertEqual(self.reservation.status, 'pending')
        self.assertEqual(str(self.reservation), f"Reserva de {self.teacher} para {self.room} às {self.hour} em 2024-08-20")

    def test_reservation_get_teacher_name(self):
        # Testa se o método get_teacher_name retorna o nome correto
        self.assertEqual(self.reservation.get_teacher_name(), "John")

    def test_reservation_approval_creation(self):
        # Testa se a criação do ReservationApproval foi bem-sucedida
        approval = ReservationApproval.objects.create(
            reservation=self.reservation,
            manager=self.manager,
            status='approved'
        )
        self.assertEqual(approval.reservation, self.reservation)
        self.assertEqual(approval.manager, self.manager)
        self.assertEqual(approval.status, 'approved')
        self.assertIsNotNone(approval.approved_at)
        self.assertEqual(str(approval), f"Aprovação de {self.manager} para a reserva {self.reservation}")

    def test_reservation_status_choices(self):
        # Testa se os choices de status estão configurados corretamente
        expected_choices = [
            ('approved', 'Aprovado'),
            ('rejected', 'Rejeitado'),
            ('cancelled', 'Cancelado'),
            ('pending', 'Pendente'),
        ]
        actual_choices = list(self.reservation._meta.get_field('status').choices)
        self.assertEqual(actual_choices, expected_choices)