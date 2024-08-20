from django.test import TestCase
from rooms.models import Room
from rooms.service import RoomService
from rooms.repository import RoomRepository
from unittest.mock import patch

class RoomServiceTest(TestCase):

    def setUp(self):
        self.room1 = Room.objects.create(name="Sala 1")
        self.room2 = Room.objects.create(name="Sala 2")
    
    def test_list_all_rooms(self):
        with patch.object(RoomRepository, 'get_all_rooms', return_value=Room.objects.all()):
            rooms = RoomService.list_all_rooms(page=1, per_page=1)
            self.assertEqual(rooms.paginator.count, 2)
            self.assertEqual(rooms.number, 1)
            self.assertEqual(rooms[0].name, "Sala 1")

    def test_get_room_details(self):
        with patch.object(RoomRepository, 'get_room_by_id', return_value=self.room1):
            room = RoomService.get_room_details(self.room1.id)
            self.assertIsNotNone(room)
            self.assertEqual(room.name, "Sala 1")

    def test_create_new_room(self):
        with patch.object(RoomRepository, 'create_room', return_value=Room.objects.create(name="Sala 3")):
            new_room = RoomService.create_new_room(name="Sala 3")
            self.assertEqual(Room.objects.count(), 3)
            self.assertEqual(new_room.name, "Sala 3")

    def test_update_existing_room(self):
        with patch.object(RoomRepository, 'update_room', return_value=self.room1) as mock_update:
            updated_room = RoomService.update_existing_room(self.room1.id, name="Sala 1 - Atualizada")
            self.room1.refresh_from_db()  # Refresh the room to ensure it has been updated
            self.assertEqual(updated_room.name, "Sala 1 - Atualizada")
            self.assertEqual(self.room1.name, "Sala 1 - Atualizada")
            mock_update.assert_called_once_with(self.room1.id, "Sala 1 - Atualizada")

    def test_delete_room(self):
        with patch.object(RoomRepository, 'delete_room', return_value=True):
            result = RoomService.delete_room(self.room1.id)
            self.assertTrue(result)
            self.assertEqual(Room.objects.count(), 1)
    
    def test_get_all_rooms(self):
        with patch.object(RoomRepository, 'get_all_rooms', return_value=Room.objects.all()):
            rooms = RoomService.get_all_rooms()
            self.assertEqual(rooms.count(), 2)

    def test_search_rooms(self):
        with patch.object(RoomRepository, 'search_rooms', return_value=Room.objects.filter(name__icontains="Sala")):
            rooms = RoomService.search_rooms("Sala", page=1, per_page=1)
            self.assertEqual(rooms.paginator.count, 2)
            self.assertEqual(rooms.number, 1)
            self.assertEqual(rooms[0].name, "Sala 1")