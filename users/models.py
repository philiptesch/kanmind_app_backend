from django.db import models
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    fullname = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)


    def __str__(self):
        return self.user.username