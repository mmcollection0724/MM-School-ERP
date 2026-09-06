from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    StudentForm,
    TeacherForm,
    ExpenseForm,
    NoticeForm,
    FeePaymentForm,
    AttendanceForm,
    ResultForm,
    TimetableForm,
    BookForm,
    BookIssueForm,
    SalaryForm,
)
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
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username", "").strip(),
            password=request.POST.get("password", ""),
        )
        if user:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Wrong username or password!")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    context = {
        "student_count": Student.objects.filter(active=True).count(),
        "teacher_count": Teacher.objects.filter(active=True).count(),
        "recent_students": Student.objects.filter(active=True)[:5],
        "expense_total": sum((x.amount for x in Expense.objects.all()), 0),
        "notices": Notice.objects.all()[:5],
    }
    return render(request, "dashboard.html", context)

@login_required
def students(request):
    q = request.GET.get("q", "").strip()
    cls = request.GET.get("class", "").strip()
    qs = Student.objects.filter(active=True)
    if q:
        qs = qs.filter(
            Q(name__icontains=q) | Q(admission_id__icontains=q) |
            Q(cnic__icontains=q) | Q(phone__icontains=q) |
            Q(guardian_phone__icontains=q)
        )
    if cls:
        qs = qs.filter(class_name=cls)
    return render(request, "students.html", {"students": qs, "q": q, "selected_class": cls})

@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            next_no = Student.objects.count() + 1
            obj.admission_id = f"MM-{next_no:03d}"
            obj.save()
            messages.success(request, "Student admission saved successfully!")
            return redirect("students")
    else:
        form = StudentForm(initial={"admission_date": timezone.localdate(), "monthly_fee": 3000})
    return render(request, "form_page.html", {"form": form, "title": "Student Admission Form", "subtitle": "Complete student admission information", "back": "students"})

@login_required
def delete_student(request, pk):
    if request.method == "POST":
        get_object_or_404(Student, pk=pk).delete()
    return redirect("students")

@login_required
def teachers(request):
    q = request.GET.get("q", "").strip()
    role = request.GET.get("role", "").strip()
    qs = Teacher.objects.filter(active=True)
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(staff_id__icontains=q) | Q(phone__icontains=q) | Q(cnic__icontains=q))
    if role:
        qs = qs.filter(role=role)
    return render(request, "teachers.html", {"teachers": qs, "q": q, "selected_role": role})

@login_required
def add_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.staff_id = f"ST-{Teacher.objects.count()+1:03d}"
            obj.save()
            messages.success(request, "Teacher / Staff added successfully!")
            return redirect("teachers")
    else:
        form = TeacherForm()
    return render(request, "form_page.html", {"form": form, "title": "Add Teacher / Staff", "subtitle": "Enter staff information", "back": "teachers"})

@login_required
def delete_teacher(request, pk):
    if request.method == "POST":
        get_object_or_404(Teacher, pk=pk).delete()
    return redirect("teachers")

@login_required
def expenses(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense saved successfully!")
            return redirect("expenses")
    else:
        form = ExpenseForm()
    return render(request, "expenses.html", {"form": form, "expenses": Expense.objects.all()})

@login_required
def notices(request):
    notices = Notice.objects.all()

    if request.method == "POST":
        form = NoticeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Notice added successfully!"
            )
            return redirect("notices")

    else:
        form = NoticeForm()

    return render(
        request,
        "notices.html",
        {
            "form": form,
            "notices": notices,
        },
    )
@login_required
def fee_collection(request):
    payments = FeePayment.objects.select_related("student").all()
    return render(request, "fee_collection.html", {"payments": payments})


@login_required
def collect_fee(request):
    if request.method == "POST":
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fee collected successfully!")
            return redirect("fee_collection")
    else:
        form = FeePaymentForm(initial={"paid_on": timezone.localdate()})

    return render(
        request,
        "form_page.html",
        {
            "form": form,
            "title": "Collect Student Fee",
            "subtitle": "Enter monthly fee payment information",
            "back": "fee_collection",
        },
    )
@login_required
def attendance(request):
    selected_class = request.GET.get("class", "").strip()
    selected_date = request.GET.get("date", "").strip()

    if not selected_date:
        selected_date = str(timezone.localdate())

    students = Student.objects.filter(active=True)

    if selected_class:
        students = students.filter(class_name=selected_class)

    records = Attendance.objects.filter(date=selected_date).select_related("student")

    if selected_class:
        records = records.filter(student__class_name=selected_class)

    attendance_map = {
        record.student_id: record
        for record in records
    }

    if request.method == "POST":
        attendance_date = request.POST.get("attendance_date")
        class_name = request.POST.get("class_name")

        if attendance_date and class_name:
            class_students = Student.objects.filter(
                active=True,
                class_name=class_name
            )

            for student in class_students:
                status = request.POST.get(f"status_{student.id}", "Present")
                remarks = request.POST.get(f"remarks_{student.id}", "").strip()

                Attendance.objects.update_or_create(
                    student=student,
                    date=attendance_date,
                    defaults={
                        "status": status,
                        "remarks": remarks,
                    },
                )

            messages.success(request, "Attendance saved successfully!")
            return redirect(
                f"/attendance/?class={class_name}&date={attendance_date}"
            )

    return render(
        request,
        "attendance.html",
        {
            "students": students,
            "attendance_map": attendance_map,
            "selected_class": selected_class,
            "selected_date": selected_date,
        },
    )
@login_required
def attendance_report(request):
    selected_class = request.GET.get("class", "").strip()
    start_date = request.GET.get("start_date", "").strip()
    end_date = request.GET.get("end_date", "").strip()

    students = Student.objects.filter(active=True)

    if selected_class:
        students = students.filter(class_name=selected_class)

    records = Attendance.objects.filter(
        student__in=students
    ).select_related("student")

    if start_date:
        records = records.filter(date__gte=start_date)

    if end_date:
        records = records.filter(date__lte=end_date)

    report = []

    for student in students:
        student_records = records.filter(student=student)

        total = student_records.count()
        present = student_records.filter(status="Present").count()
        absent = student_records.filter(status="Absent").count()
        leave = student_records.filter(status="Leave").count()

        percentage = 0

        if total > 0:
            percentage = round((present / total) * 100, 1)

        report.append({
            "student": student,
            "total": total,
            "present": present,
            "absent": absent,
            "leave": leave,
            "percentage": percentage,
        })

    return render(
        request,
        "attendance_report.html",
        {
            "report": report,
            "selected_class": selected_class,
            "start_date": start_date,
            "end_date": end_date,
        },
    )
@login_required
def results(request):
    results = Result.objects.select_related("student").all()

    if request.method == "POST":
        form = ResultForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Result saved successfully!")
            return redirect("results")
    else:
        form = ResultForm()

    return render(
        request,
        "results.html",
        {
            "form": form,
            "results": results,
        },
    )
@login_required
def timetable(request):
    timetables = Timetable.objects.all()

    if request.method == "POST":
        form = TimetableForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Timetable saved successfully!")
            return redirect("timetable")

    else:
        form = TimetableForm()

    return render(
        request,
        "timetable.html",
        {
            "form": form,
            "timetables": timetables,
        },
    )
@login_required
def library(request):
    books = Book.objects.all()
    issues = BookIssue.objects.select_related(
        "book",
        "student"
    ).all()

    book_form = BookForm()
    issue_form = BookIssueForm()

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "add_book":
            book_form = BookForm(request.POST)

            if book_form.is_valid():
                book_form.save()
                messages.success(
                    request,
                    "Book added successfully!"
                )
                return redirect("library")

        elif action == "issue_book":
            issue_form = BookIssueForm(request.POST)

            if issue_form.is_valid():
                issue = issue_form.save(commit=False)

                if issue.book.available <= 0:
                    messages.error(
                        request,
                        "This book is currently unavailable."
                    )
                else:
                    issue.book.available -= 1
                    issue.book.save()

                    issue.save()

                    messages.success(
                        request,
                        "Book issued successfully!"
                    )

                    return redirect("library")

    return render(
        request,
        "library.html",
        {
            "books": books,
            "issues": issues,
            "book_form": book_form,
            "issue_form": issue_form,
        },
    )
@login_required
def salary(request):
    salaries = Salary.objects.select_related("teacher").all()

    if request.method == "POST":
        form = SalaryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Salary record saved successfully!"
            )
            return redirect("salary")
    else:
        form = SalaryForm()

    return render(
        request,
        "salary.html",
        {
            "form": form,
            "salaries": salaries,
        },
    )
@login_required
def ai_assistant(request):

    answer = None
    question = ""

    student_count = Student.objects.filter(active=True).count()
    teacher_count = Teacher.objects.filter(active=True).count()

    total_expenses = sum(
        (x.amount for x in Expense.objects.all()),
        0
    )

    total_fees = sum(
        (x.amount for x in FeePayment.objects.all()),
        0
    )

    total_salary = sum(
        (x.amount for x in Salary.objects.filter(status="Paid")),
        0
    )

    attendance_total = Attendance.objects.count()

    attendance_present = Attendance.objects.filter(
        status="Present"
    ).count()

    attendance_percentage = 0

    if attendance_total > 0:
        attendance_percentage = round(
            (attendance_present / attendance_total) * 100,
            1
        )

    recent_notices = Notice.objects.all()[:5]

    if request.method == "POST":

        question = request.POST.get(
            "question",
            ""
        ).strip().lower()

        found_student = None

        for student in Student.objects.filter(active=True):

            full_name = student.name.lower()
            first_name = full_name.split()[0]

            if full_name in question:
                found_student = student
                break

            if first_name in question.split():
                found_student = student
                break

        # WHO PAID FEES?

        if (
            "kis bache ne fee" in question
            or "kis bache ne fees" in question
            or "kon se bache ne fee" in question
            or "kon se bache ne fees" in question
            or "kon kon ne fee" in question
            or "kon kon ne fees" in question
            or "who paid" in question
            or "who has paid" in question
            or "which student paid" in question
        ):

            payments = FeePayment.objects.select_related(
                "student"
            ).order_by("-paid_on")

            if payments.exists():

                answer = "💰 Fee paid karne wale students:\n\n"

                for payment in payments:

                    answer += (
                        f"✅ {payment.student.name} — "
                        f"Rs. {payment.amount} — "
                        f"{payment.month} — "
                        f"Paid on {payment.paid_on}\n"
                    )

            else:

                answer = (
                    "❌ Abhi kisi student ki fee payment "
                    "database mein record nahi hai."
                )

        # TOTAL FEES

        elif (
            "total fees" in question
            or "fees collected" in question
            or "total fee" in question
            or "fee collection" in question
        ):

            answer = (
                f"💰 Total recorded fee collection "
                f"Rs. {total_fees} hai."
            )

        # INDIVIDUAL STUDENT FEE

        elif (
            "fee" in question
            or "fees" in question
            or "paid" in question
        ):

            if found_student:

                payments = FeePayment.objects.filter(
                    student=found_student
                ).order_by("-paid_on")

                if payments.exists():

                    latest = payments.first()

                    answer = (
                        f"✅ Yes! {found_student.name} ki fee paid hai. "
                        f"Amount: Rs. {latest.amount}. "
                        f"Month: {latest.month}. "
                        f"Paid on: {latest.paid_on}."
                    )

                else:

                    answer = (
                        f"❌ {found_student.name} ki fee ka "
                        f"koi payment record nahi mila."
                    )

            else:

                answer = (
                    "❌ Mujhe is naam ka student nahi mila."
                )

        # STUDENTS

        elif (
            "student" in question
            or "students" in question
        ):

            answer = (
                f"👨‍🎓 School mein "
                f"{student_count} active students hain."
            )

        # TEACHERS / STAFF

        elif (
            "teacher" in question
            or "teachers" in question
            or "staff" in question
        ):

            answer = (
                f"👨‍🏫 School mein "
                f"{teacher_count} active teachers/staff hain."
            )

        # ATTENDANCE

        elif "attendance" in question:

            answer = (
                f"📊 Overall recorded attendance "
                f"{attendance_percentage}% hai."
            )

        # SALARY

        elif (
            "salary" in question
            or "salaries" in question
        ):

            answer = (
                f"💵 Total paid salaries "
                f"Rs. {total_salary} hain."
            )

        # EXPENSES

        elif (
            "expense" in question
            or "expenses" in question
        ):

            answer = (
                f"💸 Total recorded expenses "
                f"Rs. {total_expenses} hain."
            )

        else:

            answer = (
                "🤖 Main students, fees, attendance, "
                "teachers, salary aur expenses ke "
                "questions answer kar sakta hoon."
            )

    context = {
        "student_count": student_count,
        "teacher_count": teacher_count,
        "total_expenses": total_expenses,
        "total_fees": total_fees,
        "total_salary": total_salary,
        "attendance_percentage": attendance_percentage,
        "recent_notices": recent_notices,
        "answer": answer,
        "question": question,
    }

    return render(
        request,
        "ai_assistant.html",
        context
    )