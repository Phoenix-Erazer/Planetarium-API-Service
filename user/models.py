from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.username}: {self.first_name} {self.last_name}"
