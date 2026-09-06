from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("admission_id", models.CharField(max_length=30, unique=True)),
                ("name", models.CharField(max_length=150)),
                ("father", models.CharField(max_length=150)),
                ("father_cnic", models.CharField(blank=True, max_length=30)),
                ("cnic", models.CharField(blank=True, max_length=30)),
                ("dob", models.DateField(blank=True, null=True)),
                ("gender", models.CharField(default="Male", max_length=20)),
                ("class_name", models.CharField(choices=[("Nursery","Nursery"),("Prep","Prep"),("1st","1st"),("2nd","2nd"),("3rd","3rd"),("4th","4th"),("5th","5th"),("6th","6th"),("7th","7th"),("8th","8th"),("9th","9th"),("10th","10th")], max_length=20)),
                ("admission_date", models.DateField()),
                ("monthly_fee", models.DecimalField(decimal_places=2, default=3000, max_digits=10)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("guardian_phone", models.CharField(max_length=30)),
                ("emergency", models.CharField(blank=True, max_length=30)),
                ("address", models.TextField()),
                ("previous_school", models.CharField(blank=True, max_length=200)),
                ("previous_class", models.CharField(blank=True, max_length=30)),
                ("religion", models.CharField(blank=True, max_length=50)),
                ("blood", models.CharField(blank=True, max_length=10)),
                ("notes", models.TextField(blank=True)),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("staff_id", models.CharField(max_length=30, unique=True)),
                ("name", models.CharField(max_length=150)),
                ("role", models.CharField(choices=[("Teacher","Teacher"),("Administrator","Administrator"),("Accountant","Accountant"),("Staff","Staff")], max_length=30)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("cnic", models.CharField(blank=True, max_length=30)),
                ("joining_date", models.DateField(blank=True, null=True)),
                ("salary", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("description", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Notice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("text", models.TextField()),
                ("date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-date", "-created_at"]},
        ),
    ]
