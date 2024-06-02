from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class Lecture(models.Model):
    lecture_id = models.IntegerField(primary_key=True)
    lecture_name = models.CharField(max_length=100)
    position = models.IntegerField()
    lecture_is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.lecture_name

class Student(AbstractUser):
    lecture_pos = models.IntegerField(default=1)

class Task(models.Model):
    task_id = models.IntegerField(primary_key=True)
    task_name = models.CharField(max_length=100)
    task_is_solved = models.BooleanField()
    task_text = models.TextField()
    task_solution = models.TextField()
    task_max_points = models.IntegerField()
    key_statement = models.CharField(max_length=100, null=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name
    
class Points(models.Model):
    point_id = models.IntegerField(primary_key=True)
    point = models.IntegerField()
    answer = models.CharField(max_length=3000)
    comment = models.CharField(max_length=1000, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    auth_user = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_viewed = models.BooleanField(default=False)

class Question(models.Model):
    question_id = models.IntegerField(primary_key=True)
    question = models.CharField(max_length=3000, null=True)
    comment = models.CharField(max_length=1000, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    auth_user = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_viewed = models.BooleanField(default=False)
    is_viewed_student = models.BooleanField(default=False)

class StudentGroup(models.Model):
    student_group_id = models.IntegerField(primary_key=True)
    student_group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.student_group_name
