from django.contrib.auth.models import User
from django.db import models


# I would have much rather used a custom user model with a field 'language', but I was unable to
# change the user model mid-project
class UserLangauge(models.Model):

    user = models.OneToOneField(max_length=20, on_delete=models.CASCADE, to=User)
    language = models.CharField(max_length=10)

    def __str__(self):
        return self.language.__str__()