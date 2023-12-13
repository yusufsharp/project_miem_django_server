from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Player
from .serializers import PlayerSerializer
from django.contrib.auth.hashers import make_password



class IndexViewTest(TestCase):
    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/index.html')

    def test_index_view_returns_nonexistent_url(self):
        response = self.client.get(reverse('index'), {'some_param': 'lol'})
        self.assertTemplateUsed(response, 'myapp/index.html')

class PlayerViewSetTest(TestCase):
    def setUp(self):
        self.player1 = Player.objects.create(login='player1')
        self.player2 = Player.objects.create(login='player2')

        self.client = APIClient()


    def test_player_list_view(self):
        # Получаем URL для списка игроков
        url = '/api/player_info/'

        # Отправляем GET-запрос на URL
        response = self.client.get(url)

        # Проверяем, что запрос завершился успешно (код 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что полученные данные соответствуют ожидаемым данным
        expected_data = PlayerSerializer([self.player1, self.player2], many=True).data
        self.assertEqual(response.data, expected_data)

class ItemAPIViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login = 'loluser'
        self.password = 'lolpassword'
        self.player = Player.objects.create(login=self.login, password=make_password(self.password))

    def test_get_valid_password(self):
        url = reverse('item_api', kwargs={'login': self.login, 'password': self.password})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Пароль верен'})

    def test_get_invalid_password(self):
        url = reverse('item_api', kwargs={'login': self.login, 'password': 'wrong_password'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'message': 'Пароль не верен'})


class UpdateAchievesViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login = 'testuser'
        self.achieve_type = 'experience'
        self.type_value = 10
        self.player = Player.objects.create(login=self.login)

    def test_patch_achieves_success(self):
        url = reverse('update-achieves', kwargs={'login': self.login, 'achieve_type': self.achieve_type, 'type_value': self.type_value})
        key = "f@?2R{yPCZuI2!u(iE!4$Z&(}.sd;G9e4*<kd{D8ltAfs9HNqIR*0w=^#yG^):{?"

        response = self.client.patch(url, params={'key': key})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Serializer', response.data)
        self.assertIn('key', response.data)
        self.assertEqual(response.data['key'], key)

    def test_patch_achieves_invalid_key(self):
        url = reverse('update-achieves', kwargs={'login': self.login, 'achieve_type': self.achieve_type, 'type_value': self.type_value})
        key = "lol_key"

        response = self.client.patch(url, params={'key': key})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'].code, 'permission_denied')

    def test_patch_achieves_invalid_achieve_type(self):
        url = reverse('update-achieves', kwargs={'login': self.login, 'achieve_type': 'lol_type', 'type_value': self.type_value})
        key = "f@?2R{yPCZuI2!u(iE!4$Z&(}.sd;G9e4*<kd{D8ltAfs9HNqIR*0w=^#yG^):{?"

        response = self.client.patch(url, params={'key': key})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "Недопустимый тип ачивки")

    def test_patch_achieves_player_not_found(self):
        url = reverse('update-achieves', kwargs={'login': 'ANANIMUS', 'achieve_type': self.achieve_type, 'type_value': self.type_value})
        key = "f@?2R{yPCZuI2!u(iE!4$Z&(}.sd;G9e4*<kd{D8ltAfs9HNqIR*0w=^#yG^):{?"

        response = self.client.patch(url, params={'key': key})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "Игрок не найден")
