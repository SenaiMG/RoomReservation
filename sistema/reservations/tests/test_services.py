from django.test import TestCase
from django.contrib.auth import get_user_model
from reservations.models import Hour, Reservation, ReservationApproval
from rooms.models import Room
from reservations.service import ReservationService, ReservationApprovalService, HourService

User = get_user_model()

class ReservationServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        self.manager = User.objects.create_user(username="manageruser", email="manager@example.com", password="password")
        self.room = Room.objects.create(name="Sala 1")
        self.hour = Hour.objects.create(range_hour="10:00 - 11:00")
        self.reservation = Reservation.objects.create(
            room=self.room,
            teacher=self.user,
            hour=self.hour,
            date="2024-08-21",
            status="pending"
        )

    def test_create_new_reservation(self):
        new_reservation = ReservationService.create_new_reservation(
            room=self.room,
            teacher=self.user,
            hour=self.hour,
            date="2024-08-22",
            status="pending"
        )
        self.assertIsNotNone(new_reservation.id)
        self.assertEqual(new_reservation.room, self.room)
        self.assertEqual(new_reservation.teacher, self.user)
        self.assertEqual(new_reservation.status, "pending")

    def test_update_existing_reservation(self):
        updated_reservation = ReservationService.update_existing_reservation(
            self.reservation.id,
            status="approved"
        )
        self.assertEqual(updated_reservation.status, "approved")

    def test_delete_reservation(self):
        ReservationService.delete_reservation(self.reservation.id)
        reservation = Reservation.objects.filter(id=self.reservation.id).first()
        self.assertIsNone(reservation)

    def test_get_reservation_details(self):
        reservation = ReservationService.get_reservation_details(self.reservation.id)
        self.assertEqual(reservation, self.reservation)

    def test_list_all_reservations(self):
        reservations = ReservationService.list_all_reservations(page=1, per_page=10)
        self.assertEqual(reservations.object_list[0], self.reservation)

    def test_list_pending_reservations_by_date(self):
        pending_reservations = ReservationService.list_pending_reservations_by_date("2024-08-21")
        self.assertEqual(pending_reservations.count(), 1)
        self.assertEqual(pending_reservations.first(), self.reservation)

    def test_list_pending_reservations_all(self):
        pending_reservations = ReservationService.list_pending_reservations_all(page=1, per_page=10)
        self.assertEqual(pending_reservations.object_list[0], self.reservation)

    def test_list_available_hours_for_date(self):
        available_hours = ReservationService.list_available_hours_for_date(self.room, "2024-08-21")
        self.assertNotEqual(len(available_hours), 0)

    def test_get_user_reservations(self):
        reservations = ReservationService.get_user_reservations(self.user.id)
        self.assertEqual(len(reservations), 1)  # Usando len() para contar o número de itens

    def test_search_reservations(self):
        search_result = ReservationService.search_reservations("Sala 1")
        self.assertEqual(search_result['total_items'], 1)
        self.assertEqual(search_result['reservations'][0]['reservation_id'], self.reservation.id)

    def test_cancel_reservation(self):
        cancelled_reservation = ReservationService.cancel_reservation(self.reservation.id, self.manager)
        self.assertEqual(cancelled_reservation.status, "cancelled")


class ReservationApprovalServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password")
        self.manager = User.objects.create_user(username="manageruser", email="manager@example.com", password="password")
        self.room = Room.objects.create(name="Sala 1")
        self.hour = Hour.objects.create(range_hour="10:00 - 11:00")
        self.reservation = Reservation.objects.create(
            room=self.room,
            teacher=self.user,
            hour=self.hour,
            date="2024-08-21",
            status="pending"
        )
        self.approval = ReservationApproval.objects.create(
            reservation=self.reservation,
            manager=self.manager,
            status="approved"
        )

    def test_list_all_approvals(self):
        approvals = ReservationApprovalService.list_all_approvals(page=1, per_page=10)
        self.assertEqual(approvals.object_list[0], self.approval)

    def test_get_approval_details(self):
        approval = ReservationApprovalService.get_approval_details(self.approval.id)
        self.assertEqual(approval, self.approval)

    def test_create_new_approval(self):
        new_approval = ReservationApprovalService.create_new_approval(
            reservation=self.reservation,
            manager=self.manager,
            status="rejected"
        )
        self.assertIsNotNone(new_approval.id)
        self.assertEqual(new_approval.status, "rejected")


class HourServiceTest(TestCase):

    def setUp(self):
        self.hour = Hour.objects.create(range_hour="10:00 - 11:00")

    def test_list_all_hours(self):
        hours = HourService.list_all_hours(page=1, per_page=10)
        self.assertEqual(hours.object_list[0], self.hour)

    def test_get_hour_details(self):
        hour = HourService.get_hour_details(self.hour.id)
        self.assertEqual(hour, self.hour)

    def test_create_new_hour(self):
        new_hour = HourService.create_new_hour(range_hour="11:00 - 12:00")
        self.assertIsNotNone(new_hour.id)
        self.assertEqual(new_hour.range_hour, "11:00 - 12:00")

    def test_update_existing_hour(self):
        updated_hour = HourService.update_existing_hour(self.hour.id, range_hour="11:00 - 12:00")
        self.assertEqual(updated_hour.range_hour, "11:00 - 12:00")

    def test_delete_hour(self):
        HourService.delete_hour(self.hour.id)
        hour = Hour.objects.filter(id=self.hour.id).first()
        self.assertIsNone(hour)

    def test_get_all_hours(self):
        hours = HourService.get_all_hours()
        self.assertEqual(hours.count(), 1)
        self.assertEqual(hours.first(), self.hour)

    def test_get_available_hours(self):
        all_hours = HourService.get_all_hours()
        occupied_hour_ids = []
        available_hours = HourService.get_available_hours(all_hours, occupied_hour_ids)
        self.assertEqual(available_hours.count(), 1)
        self.assertEqual(available_hours.first(), self.hour)

    def test_search_hours(self):
        search_result = HourService.search_hours("10:00", page=1, per_page=10)
        self.assertEqual(search_result.object_list[0], self.hour)