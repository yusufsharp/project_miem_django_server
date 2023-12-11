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
    return render(request, 'myapp/index.html')


class PlayerViewSet(ModelViewSet):
    serializer_class = serializers.PlayerSerializer
    queryset = models.Player.objects.all()
    lookup_field = 'login'


class ItemAPIView(APIView):
    serializer_class = serializers.PlayerSerializer

    def get(self, request, login, password):
        try:
            player = get_object_or_404(models.Player, login=login)
            is_valid_password = check_password(password, player.password)

            if is_valid_password:
                return Response({'message': 'Пароль верен'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Пароль не верен'}, status=status.HTTP_401_UNAUTHORIZED)

            #return Response({'login': player.login, 'password': player.password}, status=status.HTTP_200_OK)
        except Http404:
            return Response({'error': 'Параметр login не указан'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateAchievesView(APIView):
    def patch(self, request, login, achieve_type, type_value):
        try:
            param_value = request.query_params.get('key')
            if param_value != "f@?2R{yPCZuI2!u(iE!4$Z&(}.sd;G9e4*<kd{D8ltAfs9HNqIR*0w=^#yG^):{?":
                raise PermissionDenied("You don't have permission to perform this action.")

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
