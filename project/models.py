from django.db import models
from django.conf import settings


class Project(models.Model):
    BACKEND = "B"
    FRONTEND = "F"
    IOS = "I"
    ANDROID = "A"

    TYPE = [(BACKEND, "Back-end"), (FRONTEND, "Front-end"), (IOS, "IOS"), (ANDROID, "Android")]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=2, choices=TYPE, default=BACKEND)
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="authored_projects"
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Contributors(models.Model):
    REPONSABLE = "R"
    COLLABORATEUR = "C"
    ROLE = [(REPONSABLE, "Responsable"), (COLLABORATEUR, "Collaborateur")]

    # user_id = models.IntegerField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    users_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # project_id = models.IntegerField(Project, on_delete=models.CASCADE)
    projects_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=1)
    role = models.CharField(max_length=1, choices=ROLE, default=COLLABORATEUR)


class Issues(models.Model):
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

    # project_id = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")

    status = models.CharField(max_length=2, choices=STATUS, default=A_FAIRE)
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issues_written"
    )
    assignee_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assigned_issues"
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Comments(models.Model):
    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE, related_name="comments")
    time_created = models.DateTimeField(auto_now_add=True)
