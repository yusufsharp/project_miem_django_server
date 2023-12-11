from django.db import models


class PlayerAchieves(models.Model):
    experience = models.IntegerField(default=0)
    health = models.IntegerField(default=100)
    points = models.IntegerField(default=0)
    completion_time = models.IntegerField(default=0)

    def __str__(self):
        return self.experience





class Player(models.Model):
    login = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)
    achieves = models.ForeignKey(PlayerAchieves, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.login


