from django.test import TestCase
from rooms.models import Room
from rooms.repository import RoomRepository


class RoomRepositoryTest(TestCase):

    def setUp(self):
        self.room1 = Room.objects.create(name="Sala 1")
        self.room2 = Room.objects.create(name="Sala 2")

    def test_get_all_rooms(self):
        rooms = RoomRepository.get_all_rooms()
        self.assertEqual(rooms.count(), 2)

    def test_get_room_by_id(self):
        room = RoomRepository.get_room_by_id(self.room1.id)
        self.assertEqual(room.name, "Sala 1")

    def test_create_room(self):
        new_room = RoomRepository.create_room(name="Sala 3")
        self.assertEqual(Room.objects.count(), 3)
        self.assertEqual(new_room.name, "Sala 3")

    def test_update_room(self):
        updated_room = RoomRepository.update_room(self.room1.id, name="Sala 1 - Atualizada")
        self.assertIsNotNone(updated_room)
        self.assertEqual(updated_room.name, "Sala 1 - Atualizada")

    def test_delete_room(self):
        result = RoomRepository.delete_room(self.room1.id)
        self.assertTrue(result)
        self.assertEqual(Room.objects.count(), 1)

    def test_search_rooms_by_id(self):
        rooms = RoomRepository.search_rooms(str(self.room1.id))
        self.assertEqual(rooms.count(), 1)
        self.assertEqual(rooms.first().name, "Sala 1")

    def test_search_rooms_by_name(self):
        rooms = RoomRepository.search_rooms("Sala 2")
        self.assertEqual(rooms.count(), 1)
        self.assertEqual(rooms.first().name, "Sala 2")