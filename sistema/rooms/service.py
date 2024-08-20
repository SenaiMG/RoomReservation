from rooms.repository import RoomRepository
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class RoomService:
    @staticmethod
    def list_all_rooms(page=1, per_page=10):
        """
        Lista todas as salas com paginação.

        :param page: Número da página atual.
        :param per_page: Quantidade de itens por página.
        :return: Página atual com as salas e informações de paginação.
        """
        all_rooms = RoomRepository.get_all_rooms()
        paginator = Paginator(all_rooms, per_page)

        try:
            rooms = paginator.page(page)
        except PageNotAnInteger:
            rooms = paginator.page(1)
        except EmptyPage:
            rooms = paginator.page(paginator.num_pages)

        return rooms

    @staticmethod
    def get_room_details(room_id):
        """Obtém os detalhes de uma sala específica."""
        return RoomRepository.get_room_by_id(room_id)

    @staticmethod
    def create_new_room(name):
        """Cria uma nova sala."""
        return RoomRepository.create_room(name)

    @staticmethod
    def update_existing_room(room_id, name):
        """Atualiza uma sala existente."""
        return RoomRepository.update_room(room_id, name)

    @staticmethod
    def delete_room(room_id):
        """Remove uma sala do sistema."""
        return RoomRepository.delete_room(room_id)
    
    @staticmethod
    def get_all_rooms():
        """Retorna todas as salas."""
        return RoomRepository.get_all_rooms()
    
    @staticmethod
    def search_rooms(query, page=1, per_page=10):
        """Realiza a busca de salas com paginação."""
        rooms = RoomRepository.search_rooms(query)
        paginator = Paginator(rooms, per_page)

        try:
            paginated_rooms = paginator.page(page)
        except PageNotAnInteger:
            paginated_rooms = paginator.page(1)
        except EmptyPage:
            paginated_rooms = paginator.page(paginator.num_pages)

        return paginated_rooms