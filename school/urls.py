from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("students/", views.students, name="students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/<int:pk>/delete/", views.delete_student, name="delete_student"),

    path("teachers/", views.teachers, name="teachers"),
    path("teachers/add/", views.add_teacher, name="add_teacher"),
    path("teachers/<int:pk>/delete/", views.delete_teacher, name="delete_teacher"),

    path("expenses/", views.expenses, name="expenses"),

    path("fees/", views.fee_collection, name="fee_collection"),
    path("fees/collect/", views.collect_fee, name="collect_fee"),
    path("salary/", views.salary, name="salary"),
    path("ai-assistant/", views.ai_assistant, name="ai_assistant"),

    path("notices/", views.notices, name="notices"),
    path("attendance/", views.attendance, name="attendance"),
    path("attendance-report/", views.attendance_report, name="attendance_report"),
    path("results/", views.results, name="results"),
    path("timetable/", views.timetable, name="timetable"),
    path("library/", views.library, name="library"),
    path("ai-assistant/", views.ai_assistant, name="ai_assistant"),
]