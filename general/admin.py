from django.contrib import admin

from general.models import Lecture, Task, Points, Student

# Register your models here.

admin.site.register(Student)
admin.site.register(Lecture)
admin.site.register(Task)
admin.site.register(Points)

