from rest_framework.test import APITestCase
from django.urls import reverse
from rooms.models import Room
from reservations.models import Hour, Reservation
from users.models import User

class CheckAvailableHoursAPITest(APITestCase):

    def setUp(self):
        # Criação do usuário docente
        self.user = User.objects.create_user(username='teacher', password='password', email='teacher@gmail.com', user_type='teacher')
        
        # Criação da sala e das horas
        self.room = Room.objects.create(name="Sala 1")
        self.hour1 = Hour.objects.create(range_hour="08:00 - 09:00")
        self.hour2 = Hour.objects.create(range_hour="09:00 - 10:00")
        
        # Reserva feita para a hora 1
        self.reservation = Reservation.objects.create(
            room=self.room,
            teacher=self.user,
            hour=self.hour1,
            date="2024-08-25",
            status='approved'
        )

    def test_check_available_hours(self):
        # Autenticar o usuário
        self.client.login(email= "teacher@gmail.com", password='password')
        
        # Fazendo a requisição GET para a API
        url = reverse('check-availability', args=[self.room.id, "2024-08-25"])
        response = self.client.get(url)

        # Verificando o status code da resposta
        self.assertEqual(response.status_code, 200)
        
        # Verificando o conteúdo da resposta
        available_hours = response.data['available_hours']
        self.assertEqual(len(available_hours), 1)
        self.assertEqual(available_hours[0]['id'], self.hour2.id)
        self.assertEqual(available_hours[0]['range_hour'], self.hour2.range_hour)

    def test_room_not_found(self):
        # Autenticar o usuário
        self.client.login(email= "teacher@gmail.com", password='password')
        
        # Fazendo a requisição GET para um room_id inexistente
        url = reverse('check-availability', args=[999, "2024-08-25"])
        response = self.client.get(url)

        # Verificando se a resposta é 404 (Room not found)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Room not found')