from django.contrib.auth.models import User
from django.db import models

class MemberProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_first_timer = models.BooleanField(default=True)
    last_visit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username