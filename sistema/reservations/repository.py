from reservations.models import Hour
from reservations.models import Reservation
from reservations.models import ReservationApproval
from datetime import datetime
from django.db.models import Q

class ReservationApprovalRepository:
    @staticmethod
    def get_all_approvals():
        """Retorna todas as aprovações de reservas."""
        return ReservationApproval.objects.all()

    @staticmethod
    def get_approval_by_id(approval_id):
        """Retorna uma aprovação de reserva pelo ID."""
        try:
            return ReservationApproval.objects.get(id=approval_id)
        except ReservationApproval.DoesNotExist:
            return None

    @staticmethod
    def get_approval_by_reservation(reservation_id):
        """Retorna uma aprovação de reserva pelo ID da reserva."""
        try:
            return ReservationApproval.objects.get(reservation_id=reservation_id)
        except ReservationApproval.DoesNotExist:
            return None

    @staticmethod
    def create_approval(reservation, manager, status):
        """Cria uma nova aprovação de reserva."""
        return ReservationApproval.objects.create(
            reservation=reservation,
            manager=manager,
            status=status
        )
    

    
class ReservationRepository:
    @staticmethod
    def get_all_reservations():
        """Retorna todas as reservas."""
        return Reservation.objects.all()

    @staticmethod
    def get_reservation_by_id(reservation_id):
        """Retorna uma reserva pelo ID."""
        try:
            return Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return None

    @staticmethod
    def create_reservation(room, teacher, hour, date, status='pending'):
        """Cria uma nova reserva."""
        return Reservation.objects.create(
            room=room,
            teacher=teacher,
            hour=hour,
            date=date,
            status=status
        )

    @staticmethod
    def update_reservation(reservation_id, **kwargs):
        """Atualiza uma reserva existente."""
        reservation = ReservationRepository.get_reservation_by_id(reservation_id)
        if reservation:
            for key, value in kwargs.items():
                # Verifica se o campo existe no modelo Reservation antes de tentar definir o valor
                if hasattr(reservation, key):
                    setattr(reservation, key, value)
                else:
                    print(f"Warning: '{key}' não é um campo válido para Reservation.")
            reservation.save()
            return reservation
        return None

    @staticmethod
    def delete_reservation(reservation_id):
        """Deleta uma reserva pelo ID."""
        reservation = ReservationRepository.get_reservation_by_id(reservation_id)
        if reservation:
            reservation.delete()
            return True
        return False
    
    @staticmethod
    def get_reservations_by_date_and_status(date, status):
        """Retorna reservas com um determinado status para uma data específica."""
        return Reservation.objects.filter(date=date, status=status)
    
    @staticmethod
    def get_reservations_by_status(status):
        """Retorna reservas com um determinado status específico."""
        return Reservation.objects.filter(status=status)

    @staticmethod
    def get_reservations_by_user_id(user_id):
        """Retorna reservas de um usuário específico."""
        return Reservation.objects.filter(teacher_id=user_id)
    
    @staticmethod
    def get_reservations_by_room_date_and_status(room, date, status):
        """
        Retorna reservas com um determinado status para uma sala e data específicos.

        :param room: Sala para filtrar as reservas.
        :param date: Data para filtrar as reservas.
        :param status: Status das reservas (e.g. 'approved').
        :return: Queryset de reservas filtradas.
        """
        return Reservation.objects.filter(room=room, date=date, status=status)

    @staticmethod
    def search_reservations(search_query):
        """
        Realiza a busca de reservas com base em um critério genérico:
        - Se o valor é numérico, busca por ID.
        - Se o valor é uma data no formato DD/MM/YYYY, converte para YYYY-MM-DD e busca por data.
        - Se o valor é uma string, converte para maiúsculas e busca pelo nome da sala.

        :param search_query: Valor inserido pelo usuário no campo de busca.
        :return: Queryset com as reservas encontradas.
        """
        

        reservations = Reservation.objects.all()

        # Verifica se o valor é numérico e busca por ID
        if search_query.isdigit():
            reservations = reservations.filter(id=search_query)

        else:
            # Tenta converter a data do formato DD/MM/YYYY para YYYY-MM-DD
            try:
                search_query_as_date = datetime.strptime(search_query, '%d/%m/%Y').strftime('%Y-%m-%d')
                reservations = reservations.filter(date=search_query_as_date)
            except ValueError:
                # Se não for uma data, considera como nome da sala
                reservations = reservations.filter(room__name__icontains=search_query.upper())

        return reservations

    
    @staticmethod
    def search_user_reservations(user_id, query):
        """
        Realiza a busca de reservas do usuário com base em diferentes critérios.
        
        :param user_id: ID do usuário.
        :param query: Termo de busca.
        :return: Queryset com as reservas encontradas.
        """
        # Verifica se a query é numérica para buscar por ID ou hora
        if query.isdigit():
            return Reservation.objects.filter(
                Q(id=query) |
                Q(hour__range_hour=query),
                teacher_id=user_id
            )
        
        # Verifica se a query é uma data no formato DD/MM/YYYY
        elif ReservationRepository.is_valid_date(query):
            # Converte a data para o formato do banco
            query_date = ReservationRepository.format_date(query)
            return Reservation.objects.filter(date=query_date, teacher_id=user_id)
        
        # Se for texto, pode ser nome da sala ou status
        else:
            query = query.strip().lower()
            translated_status = ReservationRepository.translate_status(query)
            return Reservation.objects.filter(
                Q(room__name__icontains=query.upper()) |
                Q(status=translated_status),
                teacher_id=user_id
            )


    @staticmethod
    def is_valid_date(date_string):
        """
        Verifica se uma string é uma data válida no formato YYYY-MM-DD.

        :param date_string: String a ser verificada.
        :return: Boolean indicando se a string é uma data válida.
        """
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False
        
    

    @staticmethod
    def translate_status(status):
        """
        Converte o status de português para inglês.

        :param status: Status em português.
        :return: Status correspondente em inglês.
        """
        status_translation = {
            'pendente': 'pending',
            'aprovado': 'approved',
            'cancelado': 'cancelled',
            'rejeitado': 'rejected'
        }
        return status_translation.get(status, status)  # Retorna o status em inglês ou o próprio status se não encontrado

    @staticmethod
    def format_date(date_string):
        """
        Formata uma data do formato DD/MM/YYYY para YYYY-MM-DD.

        :param date_string: Data no formato DD/MM/YYYY.
        :return: Data no formato YYYY-MM-DD.
        """
        date_obj = datetime.strptime(date_string, '%d/%m/%Y')
        return date_obj.strftime('%Y-%m-%d')

    @staticmethod
    def get_reservations_with_approvals():
        """
        Retorna todas as reservas com as informações de aprovação associadas.

        :return: Queryset de reservas com as informações de aprovação.
        """
        return Reservation.objects.select_related('room', 'teacher', 'hour').prefetch_related('reservationapproval_set__manager').all()


class HourRepository:
    @staticmethod
    def get_all_hours():
        """Retorna todos os horários."""
        return Hour.objects.all()

    @staticmethod
    def get_hour_by_id(hour_id):
        """Retorna um horário pelo ID."""
        try:
            return Hour.objects.get(id=hour_id)
        except Hour.DoesNotExist:
            return None

    @staticmethod
    def create_hour(range_hour):
        """Cria um novo horário."""
        return Hour.objects.create(range_hour=range_hour)

    @staticmethod
    def update_hour(hour_id, range_hour):
        """Atualiza um horário existente."""
        hour = HourRepository.get_hour_by_id(hour_id)
        if hour:
            hour.range_hour = range_hour
            hour.save()
            return hour
        return None

    @staticmethod
    def delete_hour(hour_id):
        """Deleta um horário pelo ID."""
        hour = HourRepository.get_hour_by_id(hour_id)
        if hour:
            hour.delete()
            return True
        return False
    
    @staticmethod
    def filter_hours_excluding_ids(hours, excluded_ids):
        """
        Filtra horas removendo aquelas cujos IDs estão na lista de excluídos.

        :param hours: Queryset de horas para filtrar.
        :param excluded_ids: Lista de IDs a serem excluídos.
        :return: Queryset de horas filtradas.
        """
        return hours.exclude(id__in=excluded_ids)
    
    @staticmethod
    def get_hour_by_range(range_hour):
        """Retorna um horário com base no intervalo de horas."""
        try:
            return Hour.objects.get(range_hour=range_hour)
        except Hour.DoesNotExist:
            return None
        
    @staticmethod
    def search_hours(query):
        """Busca horários por ID ou por intervalo de horas (range_hour)."""
        if query.isdigit():
            # Se o query for numérico, busca por ID
            return Hour.objects.filter(id=query)
        else:
            # Se não for numérico, busca por range_hour (intervalo de horas)
            query = query.strip()
            return Hour.objects.filter(range_hour__icontains=query)