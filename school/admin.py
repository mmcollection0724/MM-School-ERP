from django.contrib import admin
from .models import Student, Teacher, Expense, Notice

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("admission_id", "name", "class_name", "father", "guardian_phone", "active")
    search_fields = ("admission_id", "name", "cnic", "phone", "guardian_phone")
    list_filter = ("class_name", "active")

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("staff_id", "name", "role", "phone", "joining_date", "active")
    search_fields = ("staff_id", "name", "phone", "cnic")
    list_filter = ("role", "active")

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "created_at")
    search_fields = ("title", "description")

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("title", "date")
    search_fields = ("title", "text")
