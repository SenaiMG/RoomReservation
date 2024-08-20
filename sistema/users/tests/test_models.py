from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):

    def setUp(self):
        # Criação de um usuário de teste
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
            user_type='teacher'
        )

    def test_user_creation(self):
        # Verifica se o usuário foi criado corretamente
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.user_type, 'teacher')
        self.assertTrue(user.check_password('password123'))

    def test_user_type_display(self):
        # Verifica se a exibição do tipo de usuário está correta
        user = User.objects.get(username='testuser')
        self.assertEqual(user.get_user_type_display(), 'Docente')

    def test_user_str_method(self):
        # Verifica se o método __str__ retorna o formato correto
        user = User.objects.get(username='testuser')
        self.assertEqual(str(user), 'testuser (Docente)')

    def test_unique_email(self):
        # Verifica se o campo de email único está funcionando
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                email='testuser@example.com',
                password='password123',
                user_type='manager'
            )
