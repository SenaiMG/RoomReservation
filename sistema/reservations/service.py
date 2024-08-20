from reservations.repository import HourRepository
from reservations.repository  import ReservationRepository
from reservations.repository  import ReservationApprovalRepository
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class ReservationApprovalService:
    @staticmethod
    def list_all_approvals(page=1, per_page=10):
        """
        Lista todas as aprovações de reservas com paginação.

        :param page: Número da página atual.
        :param per_page: Quantidade de itens por página.
        :return: Página atual com as aprovações e informações de paginação.
        """
        all_approvals = ReservationApprovalRepository.get_all_approvals()
        paginator = Paginator(all_approvals, per_page)

        try:
            approvals = paginator.page(page)
        except PageNotAnInteger:
            approvals = paginator.page(1)
        except EmptyPage:
            approvals = paginator.page(paginator.num_pages)

        return approvals

    @staticmethod
    def get_approval_details(approval_id):
        """Obtém os detalhes de uma aprovação específica."""
        return ReservationApprovalRepository.get_approval_by_id(approval_id)

    @staticmethod
    def create_new_approval(reservation, manager, status):
        """Cria uma nova aprovação de reserva."""
        return ReservationApprovalRepository.create_approval(reservation, manager, status)
    




class ReservationService:
    @staticmethod
    def list_all_reservations(page=1, per_page=10):
        """
        Lista todas as reservas com paginação.

        :param page: Número da página atual.
        :param per_page: Quantidade de itens por página.
        :return: Página atual com as reservas e informações de paginação.
        """
        all_reservations = ReservationRepository.get_all_reservations()
        paginator = Paginator(all_reservations, per_page)

        try:
            reservations = paginator.page(page)
        except PageNotAnInteger:
            # Se a página não for um inteiro, entrega a primeira página
            reservations = paginator.page(1)
        except EmptyPage:
            # Se a página estiver fora do intervalo (e.g. 9999), entrega a última página de resultados
            reservations = paginator.page(paginator.num_pages)

        return reservations

    @staticmethod
    def get_reservation_details(reservation_id):
        """Obtém os detalhes de uma reserva específica."""
        reservation = ReservationRepository.get_reservation_by_id(reservation_id)
        if reservation:
            return reservation
        else:
            return None


    @staticmethod
    def create_new_reservation(room, teacher, hour, date, status='pending'):
        """Cria uma nova reserva."""
        return ReservationRepository.create_reservation(room, teacher, hour, date, status)

    @staticmethod
    def update_existing_reservation(reservation_id, **kwargs):
        """Atualiza uma reserva existente."""
        return ReservationRepository.update_reservation(reservation_id, **kwargs)

    @staticmethod
    def delete_reservation(reservation_id):
        """Remove uma reserva do sistema."""
        return ReservationRepository.delete_reservation(reservation_id)
    
    @staticmethod
    def approved_or_rejected_reservation(reservation_id, manager, status):
        """
        Aprova ou reprova uma reserva pendente. Atualiza o status da reserva e cria um registro de aprovação.

        :param reservation_id: ID da reserva a ser aprovada.
        :param manager: Instância do usuário gestor que está aprovando a reserva.
        :return: Reserva aprovada ou mensagem de erro.
        """
        try:
            reservation = ReservationRepository.get_reservation_by_id(reservation_id)

            if reservation.status != 'pending':
                return {"error": "Reserva não está em estado pendente."}

            # Atualiza o status da reserva para 'approved'
            updated_reservation = ReservationService.update_existing_reservation(reservation_id, status=status)

            # Cria um registro de aprovação
            ReservationApprovalService.create_new_approval(reservation=updated_reservation, manager=manager, status=status)

            return updated_reservation

        except ValueError as e :
            #print(e)
            return {"error": "Reserva não encontrada."}

    @staticmethod
    def list_pending_reservations_by_date(date):
        """
        Lista todas as reservas pendentes para uma data específica.

        :param date: Data para buscar as reservas pendentes.
        :return: Lista de reservas pendentes.
        """
        return ReservationRepository.get_reservations_by_date_and_status(date, 'pending')

    @staticmethod
    def list_pending_reservations_all(page=1, per_page=10):
        """
        Lista todas as reservas pendentes para uma data específica.

        :param date: Data para buscar as reservas pendentes.
        :return: Lista de reservas pendentes.
        """
        all_reservations = ReservationRepository.get_reservations_by_status('pending')
        paginator = Paginator(all_reservations, per_page)

        try:
            reservations = paginator.page(page)
        except PageNotAnInteger:
            reservations = paginator.page(1)
        except EmptyPage:
            reservations = paginator.page(paginator.num_pages)

        return reservations

    @staticmethod
    def list_available_hours_for_date(room, date):
        """
        Lista todas as horas disponíveis para uma sala em uma data específica.

        :param room: Sala para verificar a disponibilidade.
        :param date: Data para verificar a disponibilidade.
        :return: Lista de horas disponíveis.
        """
        # Passo 1: Obter todas as reservas aprovadas para a data e sala específica
        approved_reservations = ReservationRepository.get_reservations_by_room_date_and_status(room, date, 'approved')
        
        # Passo 2: Obter os IDs das horas que já estão reservadas
        occupied_hour_ids = approved_reservations.values_list('hour_id', flat=True)

        # Passo 3: Obter todas as horas disponíveis usando o HourService
        all_hours = HourService.get_all_hours()

        # Passo 4: Filtrar as horas disponíveis removendo as ocupadas
        available_hours = HourService.get_available_hours(all_hours, occupied_hour_ids)

        return available_hours

    @staticmethod
    def get_user_reservations(user_id, page=1, per_page=10):
        """Retorna todas as reservas de um usuário específico."""
        all_reservations = ReservationRepository.get_reservations_by_user_id(user_id)
        paginator = Paginator(all_reservations, per_page)
        try:
            reservations = paginator.page(page)
        except PageNotAnInteger:
            reservations = paginator.page(1)
        except EmptyPage:
            reservations = paginator.page(paginator.num_pages)

        return reservations
    
    @staticmethod
    def search_reservations(search_query, page=1, per_page=10):
        """
        Busca reservas com base em um critério genérico e realiza a paginação dos resultados.

        :param search_query: Valor inserido pelo usuário no campo de busca (pode ser ID, data, ou nome da sala).
        :param page: Número da página atual.
        :param per_page: Quantidade de itens por página.
        :return: Página atual com as reservas e informações de paginação.
        """
        reservations = ReservationRepository.search_reservations(search_query)
        paginator = Paginator(reservations, per_page)

        try:
            paginated_reservations = paginator.page(page)
        except PageNotAnInteger:
            paginated_reservations = paginator.page(1)
        except EmptyPage:
            paginated_reservations = paginator.page(paginator.num_pages)

        # Preparando os dados para retornar com as informações necessárias
        result = []
        for reservation in paginated_reservations:
            approval_info = reservation.reservationapproval_set.first()
            result.append({
                'reservation_id': reservation.id,
                'user_name': reservation.teacher.first_name,
                'room_name': reservation.room.name,
                'reservation_date': reservation.date,
                'reservation_hour': reservation.hour.range_hour,
                'manager_name': approval_info.manager.first_name if approval_info else None,
                'approval_status': approval_info.status if approval_info else None,
                'approval_date': approval_info.approved_at if approval_info else None
            })

        # Criar a lista de números de página
        page_range = range(1, paginator.num_pages + 1)

        return {
            'reservations': result,
            'page': page,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': paginated_reservations.has_previous(),
            'has_next': paginated_reservations.has_next(),
            'previous_page_number': paginated_reservations.previous_page_number() if paginated_reservations.has_previous() else None,
            'next_page_number': paginated_reservations.next_page_number() if paginated_reservations.has_next() else None,
            'page_range': page_range  # Adicionar o intervalo de páginas
        }
        
    @staticmethod
    def list_reservations_with_approvals(page=1, per_page=10):
        reservations = ReservationRepository.get_reservations_with_approvals()
        paginator = Paginator(reservations, per_page)

        try:
            paginated_reservations = paginator.page(page)
        except PageNotAnInteger:
            paginated_reservations = paginator.page(1)
        except EmptyPage:
            paginated_reservations = paginator.page(paginator.num_pages)

        # Preparando os dados para retornar com as informações necessárias
        result = []
        for reservation in paginated_reservations:
            approval_info = reservation.reservationapproval_set.first()
            result.append({
                'reservation_id': reservation.id,
                'user_name': reservation.teacher.first_name,
                'room_name': reservation.room.name,
                'reservation_date': reservation.date,
                'reservation_hour': reservation.hour.range_hour,
                'manager_name': approval_info.manager.first_name if approval_info else None,
                'approval_status': approval_info.status if approval_info else None,
                'approval_date': approval_info.approved_at if approval_info else None
            })

        # Criar a lista de números de página
        page_range = range(1, paginator.num_pages + 1)

        return {
            'reservations': result,
            'page': page,
            'total_pages': paginator.num_pages,
            'total_items': paginator.count,
            'has_previous': paginated_reservations.has_previous(),
            'has_next': paginated_reservations.has_next(),
            'previous_page_number': paginated_reservations.previous_page_number() if paginated_reservations.has_previous() else None,
            'next_page_number': paginated_reservations.next_page_number() if paginated_reservations.has_next() else None,
            'page_range': page_range  # Adicionar o intervalo de páginas
        }
        
    @staticmethod
    def cancel_reservation(reservation_id, manager):
        """
        Cancela uma reserva e atualiza a aprovação com o status 'cancelled'.
        
        :param reservation_id: ID da reserva a ser cancelada.
        :param manager: Instância do usuário gestor que está cancelando a reserva.
        :return: Reserva cancelada ou mensagem de erro.
        """
        try:
            # Obter a reserva
            reservation = ReservationRepository.get_reservation_by_id(reservation_id)
            if not reservation:
                return {"error": "Reserva não encontrada."}

            # Atualiza o status da reserva para 'cancelled'
            updated_reservation = ReservationService.update_existing_reservation(
                reservation_id, status='cancelled'
            )

            # Atualiza ou cria o registro de aprovação com o status 'cancelled'
            approval = ReservationApprovalRepository.get_approval_by_reservation(reservation_id)
            if approval:
                approval.status = 'cancelled'
                approval.manager = manager
                approval.save()
            else:
                # Se não houver aprovação existente, cria uma nova
                ReservationApprovalService.create_new_approval(
                    reservation=updated_reservation, 
                    manager=manager, 
                    status='cancelled'
                )

            return updated_reservation

        except ValueError as e:
            return {"error": "Erro ao cancelar a reserva."}
        
    @staticmethod
    def search_user_reservations(user_id, query, page=1, per_page=20):
        """Busca reservas do usuário com paginação."""
        reservations = ReservationRepository.search_user_reservations(user_id, query)
        paginator = Paginator(reservations, per_page)

        try:
            paginated_reservations = paginator.page(page)
        except PageNotAnInteger:
            paginated_reservations = paginator.page(1)
        except EmptyPage:
            paginated_reservations = paginator.page(paginator.num_pages)

        return paginated_reservations


class HourService:
    @staticmethod
    def list_all_hours(page=1, per_page=10):
        """
        Lista todos os horários com paginação.

        :param page: Número da página atual.
        :param per_page: Quantidade de itens por página.
        :return: Página atual com os horários e informações de paginação.
        """
        all_hours = HourRepository.get_all_hours()
        paginator = Paginator(all_hours, per_page)

        try:
            hours = paginator.page(page)
        except PageNotAnInteger:
            hours = paginator.page(1)
        except EmptyPage:
            hours = paginator.page(paginator.num_pages)

        return hours

    @staticmethod
    def get_hour_details(hour_id):
        """Obtém os detalhes de um horário específico."""
        return HourRepository.get_hour_by_id(hour_id)

    @staticmethod
    def create_new_hour(range_hour):
        """Cria um novo horário."""
        return HourRepository.create_hour(range_hour)

    @staticmethod
    def update_existing_hour(hour_id, range_hour):
        """Atualiza um horário existente."""
        return HourRepository.update_hour(hour_id, range_hour)

    @staticmethod
    def delete_hour(hour_id):
        """Remove um horário do sistema."""
        return HourRepository.delete_hour(hour_id)
    

    @staticmethod
    def get_all_hours():
        """
        Retorna todas as horas disponíveis no sistema.
        """
        return HourRepository.get_all_hours()

    @staticmethod
    def get_available_hours(all_hours, occupied_hour_ids):
        """
        Filtra as horas disponíveis removendo as ocupadas.

        :param all_hours: Queryset de todas as horas.
        :param occupied_hour_ids: Lista de IDs de horas ocupadas.
        :return: Queryset de horas disponíveis.
        """
        return HourRepository.filter_hours_excluding_ids(all_hours, occupied_hour_ids)
    
    @staticmethod
    def get_hour_id_by_range(range_hour):
        """
        Obtém o ID de um horário com base no intervalo de horas.

        :param range_hour: Intervalo de horas do horário.
        :return: ID do horário ou None se não encontrado.
        """
        hour = HourRepository.get_hour_by_range(range_hour)
        if hour:
            return hour
        else:
            return None

    @staticmethod
    def search_hours(query, page=1, per_page=10):
        """Realiza a busca de horários com paginação."""
        hours = HourRepository.search_hours(query)
        paginator = Paginator(hours, per_page)

        try:
            paginated_hours = paginator.page(page)
        except PageNotAnInteger:
            paginated_hours = paginator.page(1)
        except EmptyPage:
            paginated_hours = paginator.page(paginator.num_pages)

        return paginated_hours













"""
Formas de enviar o email:
from notifications.services import EmailService

# Exemplo de envio de um email de texto simples
EmailService.send_text_email(
    subject="Sua reserva foi confirmada",
    message="Sua reserva para a sala XYZ foi confirmada.",
    recipient_list=["usuario@example.com"]
)

# Exemplo de envio de um email com corpo HTML
EmailService.send_html_email(
    subject="Sua reserva foi confirmada",
    html_content="<h1>Reserva Confirmada</h1><p>Sua reserva para a sala XYZ foi confirmada.</p>",
    recipient_list=["usuario@example.com"]
)

# Exemplo de envio de um email com anexo e corpo HTML
EmailService.send_email_with_attachment(
    subject="Documento Importante",
    message="Veja o documento em anexo.",
    recipient_list=["usuario@example.com"],
    attachment_path="/caminho/para/anexo.pdf",
    html_message="<p>Veja o documento em anexo.</p>"
)


#exemplo de envio com template html
context = {
    'user': user,
    'room': room,
    'reservation_date': reservation_date,
    'time_slot': time_slot,
}

EmailService.send_html_email_with_template(
    subject="Confirmação de Reserva",
    template_name="emails/email_confirmacao_reserva.html",
    context=context,
    recipient_list=[user.email]
)
"""





"""
# Exemplo de uso em uma view ou API
def check_availability(request, room_id, date):
    room = Room.objects.get(id=room_id)
    available_hours = ReservationService.list_available_hours_for_date(room, date)

    return JsonResponse({
        'available_hours': list(available_hours.values('id', 'range_hour'))
    })
"""