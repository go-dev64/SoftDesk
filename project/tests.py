from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from .models import Project


class TestProject(APITestCase):
    url = reverse_lazy("projects-list")

    """ pas utile pour le moment...
    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")"""

    def test_create(self):
        # Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
        self.assertFalse(Project.objects.exists())
        response = self.client.post(self.url, data={"title": "Tentive"})
        # Verifions que le stautus code est bien en erreur et nous empeche de créer le projet
        self.assertEqual(response.status_code, 405)
        # Verif qu'aucun projet n est creer malgre le status code  405
        self.assertFalse(Project.objects.exists())
