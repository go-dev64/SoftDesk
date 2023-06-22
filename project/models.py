from django.db import models

from authentication.models import User

# Create your models here.


class Project:
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class Contributors:
    user_id = models.IntegerField(
        User,
    )
    project_id = models.IntegerField(
        Project,
    )
    permission = models.ChoiceField()
    role = models.CharField()
