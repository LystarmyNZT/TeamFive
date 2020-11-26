from django.contrib import admin

# Register your models here.
from .models import stu,institute,teacher

admin.site.register(stu)
admin.site.register(institute)
admin.site.register(teacher)