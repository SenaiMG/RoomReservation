from rest_framework.response import Response
from rest_framework.decorators import api_view
from reservations.service import ReservationService
from rooms.service import RoomService
from rooms.models import Room

#@login_required(login_url='/login/') 
@api_view(['GET'])
def check_available_hours(request, room_id, date):
    try:
        room = RoomService.get_room_details(room_id)
        if not room:
            return Response({'error': 'Room not found'}, status=404)
        available_hours = ReservationService.list_available_hours_for_date(room, date)
        return Response({
            'available_hours': list(available_hours.values('id', 'range_hour'))
        })
    except Room.DoesNotExist:
        return Response({'error': 'Room not found'}, status=404)