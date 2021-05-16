from django.db import models as models


class FriendError(Exception):
    def __init__(self, message):
        self.message = message


class FriendlyUser(models.Model):
    username = models.CharField('username', max_length=20)

    def __str__(self):
        return self.username


class Friendship(models.Model):
    date = models.DateTimeField()
    friend1 = models.ForeignKey(FriendlyUser, on_delete=models.CASCADE, related_name='friend1')
    friend2 = models.ForeignKey(FriendlyUser, on_delete=models.CASCADE, related_name='friend2')

    def __str__(self):
        return str(self.friend1) + ' and ' + str(self.friend2)
