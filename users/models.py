from django.db import models

# Create your models here.


class institute(models.Model):
    iname=models.CharField(max_length=100)
    ideanid=models.CharField(max_length=100)
    iinstrid=models.CharField(max_length=100)
    def __str__(self):
        return self.iname

class teacher(models.Model):
    tid=models.CharField(max_length=100)
    tins=models.ForeignKey(institute,on_delete=models.CASCADE)
    tname=models.CharField(max_length=100)
    trole=models.CharField(max_length=100)
    tphone = models.CharField(max_length=100)
    tpassword = models.CharField(max_length=300)
    def __str__(self):
        return self.tname

class stu(models.Model):
    sid = models.CharField(max_length=100)
    sname = models.CharField(max_length=100)
    sinstitute = models.ForeignKey(institute, on_delete=models.CASCADE)
    ssupervisor = models.ForeignKey(teacher, on_delete=models.CASCADE)
    sphone = models.CharField(max_length=100)
    spassword = models.CharField(max_length=300)
    def __str__(self):
        return self.sname