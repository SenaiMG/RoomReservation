from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rooms.views import *

class RoomUrlsTest(SimpleTestCase):

    def test_all_rooms_url_resolves(self):
        url = reverse('all_rooms')
        self.assertEqual(resolve(url).func.view_class, RoomListView)

    def test_create_rooms_url_resolves(self):
        url = reverse('create_rooms')
        self.assertEqual(resolve(url).func.view_class, RoomCreateView)

    def test_edit_rooms_url_resolves(self):
        url = reverse('edit_rooms', kwargs={'rooms_id': 1})
        self.assertEqual(resolve(url).func.view_class, RoomUpdateView)

    def test_delete_rooms_url_resolves(self):
        url = reverse('delete_rooms', kwargs={'rooms_id': 1})
        self.assertEqual(resolve(url).func.view_class, RoomDeleteView)