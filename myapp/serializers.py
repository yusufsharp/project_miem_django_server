from rest_framework import serializers
from .models import Player, PlayerAchieves
from django.contrib.auth.hashers import make_password


class PlayerAchievesSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели PlayerAchieves.

    :param Meta: Класс метаданных для указания модели и полей.
    :type Meta: class
    :raises ValidationError: Если данные не соответствуют ожидаемому формату.
    """
    class Meta:
        model = PlayerAchieves
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Player.

    :param login: Логин игрока.
    :type login: str
    :param password: Пароль игрока.
    :type password: str
    :param achieves: Сериализатор ачивок игрока.
    :type achieves: PlayerAchievesSerializer
    :param Meta: Класс метаданных для указания модели и полей.
    :type Meta: class
    :raises ValidationError: Если данные не соответствуют ожидаемому формату.
    """
    login = serializers.CharField(max_length=30)
    password = serializers.CharField()
    achieves = PlayerAchievesSerializer(required=False)

    def create(self, validated_data):
        """
        Метод для создания нового игрока.

        :param validated_data: Валидированные данные для создания игрока.
        :type validated_data: dict
        :return: Объект игрока.
        :rtype: myapp.models.Player
        :raises ValidationError: Если данные не соответствуют ожидаемому формату.
        """
        player_achieves_data = validated_data.pop('achieves', None)
        achieves_instance = PlayerAchieves.objects.create(**player_achieves_data)

        validated_data['password'] = make_password(validated_data['password'])
        return Player.objects.create(achieves=achieves_instance, **validated_data)

    class Meta:
        model = Player
        fields = '__all__'
