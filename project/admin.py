from django.contrib import admin
from .models import Comments, Contributors, Issues, Project

# Register your models here.
admin.site.register(Project)
admin.site.register(Comments)
admin.site.register(Issues)
admin.site.register(Contributors)
