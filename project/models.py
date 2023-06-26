from django.db import models
from django.conf import settings


class Project:
    BACKEND = "B"
    FRONTEND = "F"
    IOS = "I"
    ANDROID = "A"

    TYPE = [(BACKEND, "Back-end"), (FRONTEND, "Front-end"), (IOS, "IOS"), (ANDROID, "Android")]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=2, choices=TYPE, default=BACKEND)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, through="Contributors", on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class Contributors:
    REPONSABLE = "R"
    COLLABORATEUR = "C"
    ROLE = [(REPONSABLE, "Responsable"), (COLLABORATEUR, "Collaborateur")]

    user_id = models.IntegerField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_id = models.IntegerField(Project, on_delete=models.CASCADE)
    permission = models.ChoiceField()
    role = models.CharField(max_length=1, choices=ROLE, default=COLLABORATEUR)


class Issues:
    FAIBLE = "F"
    MOYENNE = "M"
    ELEVEE = "E"
    PRIORITY = [(FAIBLE, "Faible"), (MOYENNE, "Moyenne"), (ELEVEE, "Elevée")]

    BUG = "B"
    AMELIARATION = "A"
    TACHE = "T"
    BALISE = [(BUG, "Bug"), (AMELIARATION, "Amélioration"), (TACHE, "Tâche")]

    A_FAIRE = "A"
    EN_COURS = "E"
    TERMINE = "T"
    STATUS = [(A_FAIRE, "A  faire"), (EN_COURS, "En cours"), (TERMINE, "Terminé")]

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=2048)
    tag = models.CharField(max_length=2, choices=BALISE, default=BUG)
    prority = models.CharField(max_length=2, choices=PRIORITY, default=ELEVEE)
    project_id = models.IntegerField()
    status = models.CharField(max_length=2, choices=STATUS, default=A_FAIRE)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee_user_id = author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class Comments:
    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = project_id = models.IntegerField()
    time_created = models.DateTimeField(auto_now_add=True)
