from django.test import TestCase
from users.models import User
from users.repository import UserRepository
from rooms.models import Room
from reservations.models import Hour, Reservation, ReservationApproval
from reservations.repository import ReservationApprovalRepository, ReservationRepository, HourRepository
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

class ReservationApprovalRepositoryTest(TestCase):
    def setUp(self):
        # Criação do usuário
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        
        # Criação da sala
        self.room = Room.objects.create(name="Sala 1")
        
        # Criação do horário
        self.hour = Hour.objects.create(range_hour="10:00-11:00")
        
        # Criação da reserva
        self.reservation = Reservation.objects.create(
            room=self.room,
            teacher=self.user,
            hour=self.hour,
            date="2024-08-20",
            status="pending"
        )

        # Criação da aprovação
        self.approval = ReservationApproval.objects.create(
            reservation=self.reservation,
            manager=self.user,
            status="approved"
        )

    def test_get_all_approvals(self):
        approvals = ReservationApprovalRepository.get_all_approvals()
        self.assertIn(self.approval, approvals)

    def test_get_approval_by_id(self):
        approval = ReservationApprovalRepository.get_approval_by_id(self.approval.id)
        self.assertEqual(approval, self.approval)

    def test_get_approval_by_reservation(self):
        approval = ReservationApprovalRepository.get_approval_by_reservation(self.reservation.id)
        self.assertEqual(approval, self.approval)

    def test_create_approval(self):
        new_approval = ReservationApprovalRepository.create_approval(self.reservation, self.user, "approved")
        self.assertIsNotNone(new_approval.id)
        self.assertEqual(new_approval.reservation, self.reservation)
        self.assertEqual(new_approval.manager, self.user)
        self.assertEqual(new_approval.status, "approved")

class ReservationRepositoryTest(TestCase):

    def setUp(self):
        self.room = Room.objects.create(name="Sala 1")
        self.user = User.objects.create_user(username="testuser",first_name="Jose Maria", email="test@example.com", password="password")
        self.hour = Hour.objects.create(range_hour="08:00 - 09:00")
        self.reservation = Reservation.objects.create(
            room=self.room,
            teacher=self.user,
            hour=self.hour,
            date="2024-08-25",
            status="pending"
        )

    def test_create_reservation(self):
        new_reservation = ReservationRepository.create_reservation(
            room=self.room,  # Passe a instância do Room aqui
            teacher=self.user,
            hour=self.hour,
            date="2024-08-21",
            status="pending"
        )
        self.assertIsNotNone(new_reservation.id)
        self.assertEqual(new_reservation.room, self.room)  # Compare com a instância do Room
        self.assertEqual(new_reservation.teacher, self.user)
        self.assertEqual(new_reservation.status, "pending")

    def test_get_all_reservations(self):
        reservations = ReservationRepository.get_all_reservations()
        self.assertEqual(len(reservations), 1)

    def test_get_reservation_by_id(self):
        fetched_reservation = ReservationRepository.get_reservation_by_id(self.reservation.id)
        self.assertEqual(fetched_reservation, self.reservation)

    def test_update_reservation(self):
        new_room = Room.objects.create(name="Sala 3")
        updated_reservation = ReservationRepository.update_reservation(
            self.reservation.id,
            room=new_room,  # Passe a instância do novo Room
            status='approved'
        )
        self.assertEqual(updated_reservation.room, new_room)
        self.assertEqual(updated_reservation.status, 'approved')

    def test_delete_reservation(self):
        result = ReservationRepository.delete_reservation(self.reservation.id)
        self.assertTrue(result)
        self.assertIsNone(ReservationRepository.get_reservation_by_id(self.reservation.id))


class HourRepositoryTest(TestCase):

    def setUp(self):
        self.hour = Hour.objects.create(range_hour="08:00 - 09:00")

    def test_create_hour(self):
        new_hour = HourRepository.create_hour("09:00 - 10:00")
        self.assertEqual(new_hour.range_hour, "09:00 - 10:00")

    def test_get_all_hours(self):
        hours = HourRepository.get_all_hours()
        self.assertEqual(len(hours), 1)

    def test_get_hour_by_id(self):
        fetched_hour = HourRepository.get_hour_by_id(self.hour.id)
        self.assertEqual(fetched_hour, self.hour)

    def test_update_hour(self):
        updated_hour = HourRepository.update_hour(self.hour.id, "10:00 - 11:00")
        self.assertEqual(updated_hour.range_hour, "10:00 - 11:00")

    def test_delete_hour(self):
        result = HourRepository.delete_hour(self.hour.id)
        self.assertTrue(result)
        self.assertIsNone(HourRepository.get_hour_by_id(self.hour.id))

    def test_search_hours_by_id(self):
        results = HourRepository.search_hours(str(self.hour.id))
        self.assertIn(self.hour, results)

    def test_search_hours_by_range(self):
        results = HourRepository.search_hours("08:00")
        self.assertIn(self.hour, results)




class UserRepositoryTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", first_name="Alice", email="alice@example.com", password="password")
        self.user2 = User.objects.create_user(username="user2", first_name="Bob", email="bob@example.com", password="password")

    def test_get_all_users(self):
        users = UserRepository.get_all_users()
        self.assertEqual(users.count(), 2)

    def test_get_user_by_id(self):
        user = UserRepository.get_user_by_id(self.user1.id)
        self.assertEqual(user.first_name, "Alice")

    def test_create_user(self):
        new_user = UserRepository.create_user(username="user3", first_name="Charlie", email="charlie@example.com", password="password")
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(new_user.first_name, "Charlie")

    def test_update_user(self):
        updated_user = UserRepository.update_user(self.user1.id, first_name="Alice Updated")
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.first_name, "Alice Updated")

    def test_delete_user(self):
        result = UserRepository.delete_user(self.user1.id)
        self.assertTrue(result)
        self.assertEqual(User.objects.count(), 1)

    def test_search_users_by_first_name(self):
        users = UserRepository.search_users("Alice")
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first().email, "alice@example.com")

    def test_search_users_by_email(self):
        users = UserRepository.search_users("bob@example.com")
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first().first_name, "Bob")