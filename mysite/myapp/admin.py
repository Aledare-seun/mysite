from django.contrib import admin
from .models import Student

# Register your models here.
class Admin(admin.ModelAdmin):
    search_fields = ('name', 'department', 'level')
    list_display = ('name', 'department', 'level')
    list_filter = ('department',)
admin.site.register(Student, Admin)
