from users.repository import UserRepository
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class UserService:
    @staticmethod
    @staticmethod
    def list_all_users(page=1, per_page=10):
        """
        Lista todos os usuários com paginação.

        :param page: Número da página atual.
        :param per_page: Quantidade de itens por página.
        :return: Página atual com os usuários e informações de paginação.
        """
        all_users = UserRepository.get_all_users()
        paginator = Paginator(all_users, per_page)

        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        return users

    @staticmethod
    def get_user_details(user_id):
        """Obtém os detalhes de um usuário específico."""
        try:
            return UserRepository.get_user_by_id(user_id)
        except UserRepository.DoesNotExist:
            return None

    @staticmethod
    def create_new_user(first_name, email, password, user_type):
        """
        Cria um novo usuário com `first_name` salvo no campo correto e gera um `username`.
        """
        username = first_name.replace(' ', '_').lower()
        user = UserRepository.create_user(
            first_name=first_name.capitalize(),
            username=username,
            email=email,
            user_type=user_type
        )
        user.set_password(password)
        user.save()
        return user

    @staticmethod
    def update_existing_user(user_id, **kwargs):
        """Atualiza um usuário existente."""
        return UserRepository.update_user(user_id, **kwargs)

    @staticmethod
    def delete_user(user_id):
        """Remove um usuário do sistema."""
        return UserRepository.delete_user(user_id)
    
    @staticmethod
    def get_all_users():
        """Retorna todos os usuários."""
        return UserRepository.get_all_users()
    

    @staticmethod
    def search_users(search_query, page=1, per_page=10):
        """
        Busca usuários pelo first_name ou email e realiza a paginação dos resultados.

        :param search_query: Termo de busca inserido pelo usuário.
        :param page: Número da página atual.
        :param per_page: Quantidade de itens por página.
        :return: Página atual com os usuários e informações de paginação.
        """
        users = UserRepository.search_users(search_query)
        paginator = Paginator(users, per_page)

        try:
            paginated_users = paginator.page(page)
        except PageNotAnInteger:
            paginated_users = paginator.page(1)
        except EmptyPage:
            paginated_users = paginator.page(paginator.num_pages)

        return paginated_users