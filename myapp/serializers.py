from rest_framework import serializers
from .models import Player, PlayerAchieves
from django.contrib.auth.hashers import make_password


class PlayerAchievesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerAchieves
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    login = serializers.CharField(max_length=30)
    password = serializers.CharField()
    achieves = PlayerAchievesSerializer(required=False)

    def create(self, validated_data):
        player_achieves_data = validated_data.pop('achieves', None)
        achieves_instance = PlayerAchieves.objects.create(**player_achieves_data)

        validated_data['password'] = make_password(validated_data['password'])
        return Player.objects.create(achieves=achieves_instance, **validated_data)

    class Meta:
        model = Player
        fields = '__all__'
