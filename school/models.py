from django.db import models

CLASSES = [
    ("Nursery", "Nursery"), ("Prep", "Prep"),
    ("1st", "1st"), ("2nd", "2nd"), ("3rd", "3rd"),
    ("4th", "4th"), ("5th", "5th"), ("6th", "6th"),
    ("7th", "7th"), ("8th", "8th"), ("9th", "9th"), ("10th", "10th"),
]

class Student(models.Model):
    admission_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    father = models.CharField(max_length=150)
    father_cnic = models.CharField(max_length=30, blank=True)
    cnic = models.CharField(max_length=30, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, default="Male")
    class_name = models.CharField(max_length=20, choices=CLASSES)
    admission_date = models.DateField()
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2, default=3000)
    phone = models.CharField(max_length=30, blank=True)
    guardian_phone = models.CharField(max_length=30)
    emergency = models.CharField(max_length=30, blank=True)
    address = models.TextField()
    previous_school = models.CharField(max_length=200, blank=True)
    previous_class = models.CharField(max_length=30, blank=True)
    religion = models.CharField(max_length=50, blank=True)
    blood = models.CharField(max_length=10, blank=True)
    notes = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.admission_id} - {self.name}"


class Teacher(models.Model):
    ROLE_CHOICES = [
        ("Teacher", "Teacher"),
        ("Administrator", "Administrator"),
        ("Accountant", "Accountant"),
        ("Staff", "Staff"),
    ]
    staff_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=30, blank=True)
    cnic = models.CharField(max_length=30, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.staff_id} - {self.name}"

class Salary(models.Model):
    STATUS_CHOICES = [
        ("Paid", "Paid"),
        ("Pending", "Pending"),
    ]

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="salary_records"
    )
    month = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.teacher.name} - {self.month}"


class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class Notice(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

class FeePayment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fee_payments")
    month = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-paid_on", "-created_at"]

    def __str__(self):
        return f"{self.student.name} - {self.month} - Rs. {self.amount}"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ("Present", "Present"),
        ("Absent", "Absent"),
        ("Leave", "Leave"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Present"
    )
    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "student__name"]

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
class Result(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="results"
    )
    subject = models.CharField(max_length=100)
    exam = models.CharField(max_length=100, default="Final Term")
    total_marks = models.PositiveIntegerField(default=100)
    obtained_marks = models.PositiveIntegerField(default=0)
    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["student__name", "subject"]

    def __str__(self):
        return f"{self.student.name} - {self.subject}"
class Timetable(models.Model):
    DAY_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
    ]

    class_name = models.CharField(max_length=20, choices=CLASSES)
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    period = models.PositiveIntegerField(default=1)
    subject = models.CharField(max_length=100)
    teacher = models.CharField(max_length=150)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["class_name", "day", "period"]

    def __str__(self):
        return f"{self.class_name} - {self.day} - {self.subject}"
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=50, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    available = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class BookIssue(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="issues"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="book_issues"
    )
    issue_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-issue_date", "-created_at"]

    def __str__(self):
        return f"{self.book.title} - {self.student.name}"
