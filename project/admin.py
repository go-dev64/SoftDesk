from django.contrib import admin
from .models import Project, Comments, Issues

# Register your models here.
admin.site.register(Project)
admin.site.register(Comments)
admin.site.register(Issues)
