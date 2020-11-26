from django.db import models

# Create your models here.
from users.models import stu,institute,teacher

class reqforleave(models.Model):
    stu = models.ForeignKey(stu, on_delete=models.CASCADE)
    reason = models.CharField(max_length=300)
    destin = models.CharField(max_length=300)
    timestart = models.CharField(max_length=300)
    timefinish = models.CharField(max_length=300)
    process1 = models.BooleanField(default=0)
    process2 = models.BooleanField(default=0)
    process3 = models.BooleanField(default=0)
    is_finished = models.BooleanField(default=0)
    def __str__(self):
        return self.stu.sname