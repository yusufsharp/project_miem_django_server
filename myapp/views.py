from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from . import models, serializers
from django.contrib.auth.hashers import check_password


def index(request):
    """
    Отображает главную страницу приложения.

    :param request: Объект запроса Django.
    :type request: django.http.HttpRequest
    :return: Объект ответа Django с отображением главной страницы.
    :rtype: django.http.HttpResponse
    """
    return render(request, 'myapp/index.html')


class PlayerViewSet(ModelViewSet):
    """
    Представление для взаимодействия с моделью Player.

    :param serializer_class: Класс сериализатора для модели Player.
    :type serializer_class: serializers.PlayerSerializer
    :param queryset: Запрос для получения всех объектов модели Player.
    :type queryset: django.db.models.query.QuerySet
    :param lookup_field: Поле для поиска объекта модели Player.
    :type lookup_field: str
        """
    serializer_class = serializers.PlayerSerializer
    queryset = models.Player.objects.all()
    lookup_field = 'login'


class ItemAPIView(APIView):
    """
    API-представление для взаимодействия с объектами Player.

    :param serializer_class: Класс сериализатора для модели Player.
    :type serializer_class: serializers.PlayerSerializer
        """
    serializer_class = serializers.PlayerSerializer

    def get(self, request, login, password):
        """
        Обработчик GET-запроса для проверки пароля игрока.

        :param request: Объект запроса Django.
        :type request: django.http.HttpRequest
        :param login: Логин игрока.
        :type login: str
        :param password: Пароль игрока.
        :type password: str
        :return: Ответ с результатом проверки пароля.
        :rtype: rest_framework.response.Response
        :raises Http404: Если параметр login не указан.
            """
        try:
            player = get_object_or_404(models.Player, login=login)
            is_valid_password = check_password(password, player.password)

            if is_valid_password:
                return Response({'message': 'Пароль верен'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Пароль не верен'}, status=status.HTTP_401_UNAUTHORIZED)

        except Http404:
            return Response({'error': 'Параметр login не указан'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Обработчик POST-запроса для создания нового игрока.

        :param request: Объект запроса Django.
        :type request: django.http.HttpRequest
        :return: Ответ с результатом создания игрока.
        :rtype: rest_framework.response.Response
        :raises serializers.ValidationError: Если данные некорректны.
            """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateAchievesView(APIView):
    """
    API-представление для обновления ачивок игрока.

    :param request: Объект запроса Django.
    :type request: django.http.HttpRequest
    :param login: Логин игрока.
    :type login: str
    :param achieve_type: Тип ачивки (experience, health, points, completion_time).
    :type achieve_type: str
    :param type_value: Значение, на которое нужно обновить ачивку.
    :type type_value: str
        """
    def patch(self, request, login, achieve_type, type_value):
        """
        Обработчик PATCH-запроса для обновления ачивок игрока.

        :param request: Объект запроса Django.
        :type request: django.http.HttpRequest
        :param login: Логин игрока.
        :type login: str
        :param achieve_type: Тип ачивки (experience, health, points, completion_time).
        :type achieve_type: str
        :param type_value: Значение, на которое нужно обновить ачивку.
        :type type_value: str
        :return: Ответ с результатом обновления ачивок.
        :rtype: rest_framework.response.Response
        :raises PermissionDenied: Если отсутствует разрешение для выполнения запроса.
        :raises models.Player.DoesNotExist: Если игрок не найден.
        :raises serializers.ValidationError: Если передан недопустимый тип ачивки.
            """
        try:
            param_value = request.query_params.get('key')
            if param_value != "f@?2R{yPCZuI2!u(iE!4$Z&(}.sd;G9e4*<kd{D8ltAfs9HNqIR*0w=^#yG^):{?":
                raise PermissionDenied("У вас нет разрешения для выполнения данного запроса!")

            player = models.Player.objects.get(login=login)
            achieves = player.achieves
            # Изменяем значение переменной в achieves в зависимости от achieve_type
            if achieve_type == 'experience':
                achieves.experience += int(type_value)
            elif achieve_type == 'health':
                achieves.health += int(type_value)
            elif achieve_type == 'points':
                achieves.points += int(type_value)
            elif achieve_type == 'completion_time':
                achieves.completion_time += int(type_value)
            else:
                return Response({"error": "Недопустимый тип ачивки"}, status=status.HTTP_400_BAD_REQUEST)

            achieves.save()

            serializer = serializers.PlayerAchievesSerializer(achieves)
            return Response({'Serializer': serializer.data, 'key': param_value}, status=status.HTTP_200_OK)

        except models.Player.DoesNotExist:
            return Response({"error": "Игрок не найден"}, status=status.HTTP_404_NOT_FOUND)
