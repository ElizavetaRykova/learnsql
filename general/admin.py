from django.contrib import admin

from general.models import Lecture, Task, Points

# Register your models here.

admin.site.register(Lecture)
admin.site.register(Task)
admin.site.register(Points)

