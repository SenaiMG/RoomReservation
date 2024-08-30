from django.db import models
from users.models import User 
from rooms.models import Room

class Hour(models.Model):
    range_hour = models.CharField(max_length=50)

    def __str__(self):
        return self.range_hour


class Reservation(models.Model):
    STATUS_CHOICES = (
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('cancelled', 'Cancelado'),
        ('pending', 'Pendente'),
    )

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, limit_choices_to={'type_user': 'teacher'}, on_delete=models.CASCADE)
    hour = models.ForeignKey(Hour, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Reserva de {self.teacher} para {self.room} às {self.hour} em {self.date}"
    
    def get_teacher_name(self):
        return self.teacher.first_name
    
    def get_teacher_email(self):
        return self.teacher.email
    
    def get_room_name(self):
        return self.room.name
    
    def get_hour_range(self):
        return self.hour.range_hour

class ReservationApproval(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, limit_choices_to={'type_user': 'manager'}, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Reservation.STATUS_CHOICES)
    approved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Aprovação de {self.manager} para a reserva {self.reservation}"