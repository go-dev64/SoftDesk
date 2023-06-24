from django.db import models

from authentication.models import User


class Project:
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=128)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, through="Contributors")
    time_created = models.DateTimeField(auto_now_add=True)


class Contributors:
    REPONSABLE = "R"
    COLLABORATEUR = "C"
    ROLE = [(REPONSABLE, "Responsable"), (COLLABORATEUR, "Collaborateur")]

    user_id = models.IntegerField(User, on_delete=models.CASCADE)
    project_id = models.IntegerField(Project, on_delete=models.CASCADE)
    permission = models.ChoiceField()
    role = models.CharField(max_length=1, choices=ROLE, default=COLLABORATEUR)


class Issues:
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=2048)
    tag = models.CharField(max_length=120)
    prority = models.CharField(max_length=50)
    project_id = models.IntegerField()
    status = models.CharField(max_length=50)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    assignee_user_id = author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class Comments:
    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = project_id = models.IntegerField()
    time_created = models.DateTimeField(auto_now_add=True)
