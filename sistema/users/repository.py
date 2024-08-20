from users.models import User
from django.db import models


class UserRepository:
    @staticmethod
    def get_all_users():
        """Retorna todos os usuários."""
        return User.objects.all()

    @staticmethod
    def get_user_by_id(user_id):
        """Retorna um usuário pelo ID."""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_users_by_type(user_type):
        """Retorna usuários pelo tipo (manager ou teacher)."""
        return User.objects.filter(user_type=user_type)

    @staticmethod
    def create_user(**kwargs):
        """Cria um novo usuário."""
        return User.objects.create(**kwargs)

    @staticmethod
    def update_user(user_id, **kwargs):
        """Atualiza um usuário existente."""
        user = UserRepository.get_user_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            user.save()
            return user
        return None

    @staticmethod
    def delete_user(user_id):
        """Deleta um usuário pelo ID."""
        user = UserRepository.get_user_by_id(user_id)
        if user:
            user.delete()
            return True
        return False
    
    @staticmethod
    def search_users(search_query):
        """
        Realiza a busca de usuários pelo first_name ou email.

        :param search_query: Termo de busca.
        :return: Queryset de usuários encontrados.
        """
        return User.objects.filter(
            models.Q(first_name__icontains=search_query) | 
            models.Q(email__icontains=search_query)
        )