from django import forms
from .models import (
    Student,
    Teacher,
    Expense,
    Notice,
    FeePayment,
    Attendance,
    Result,
    Timetable,
    Book,
    BookIssue,
    Salary,
)
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"
        exclude = ["admission_id", "active", "created_at"]
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "admission_date": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"
        exclude = ["staff_id", "active", "created_at"]
        widgets = {"joining_date": forms.DateInput(attrs={"type": "date"})}

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "amount", "description"]

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ["title", "date", "text"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}
class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = ["student", "month", "amount", "paid_on", "notes"]
        widgets = {
            "paid_on": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }
class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["student", "date", "status", "remarks"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "remarks": forms.TextInput(
                attrs={"placeholder": "Optional remarks"}
            ),
        }
class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [
            "student",
            "subject",
            "exam",
            "total_marks",
            "obtained_marks",
            "remarks",
        ]
        widgets = {
            "remarks": forms.TextInput(
                attrs={"placeholder": "Optional remarks"}
            ),
        }
class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = [
            "class_name",
            "day",
            "period",
            "subject",
            "teacher",
            "start_time",
            "end_time",
        ]
        widgets = {
            "start_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
            "end_time": forms.TimeInput(
                attrs={"type": "time"}
            ),
        }
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "category",
            "isbn",
            "quantity",
            "available",
        ]


class BookIssueForm(forms.ModelForm):
    class Meta:
        model = BookIssue
        fields = [
            "book",
            "student",
            "issue_date",
            "return_date",
            "returned",
        ]
        widgets = {
            "issue_date": forms.DateInput(attrs={"type": "date"}),
            "return_date": forms.DateInput(attrs={"type": "date"}),
        }
class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = [
            "teacher",
            "month",
            "amount",
            "paid_on",
            "status",
            "notes",
        ]
        widgets = {
            "paid_on": forms.DateInput(
                attrs={"type": "date"}
            ),
            "notes": forms.TextInput(
                attrs={"placeholder": "Optional notes"}
            ),
        }