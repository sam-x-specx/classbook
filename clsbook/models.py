# # clsbook/models.py
# from django.db import models
# from django.contrib.auth.hashers import make_password, check_password

# class ClassBook(models.Model):
#     class_name = models.CharField(max_length=50) 
#     section = models.CharField(max_length=10)
#     teacher_name = models.CharField(max_length=100)
#     password_hash = models.CharField(max_length=128)

#     def set_password(self, raw_password):
#         self.password_hash = make_password(raw_password)

#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password_hash)

#     def __str__(self):
#         return f"{self.class_name} - {self.section} ({self.teacher_name})"

# class Student(models.Model):
#     class_book = models.ForeignKey(ClassBook, on_delete=models.CASCADE, related_name='students')
#     first_name = models.CharField(max_length=50)
#     middle_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50)
#     phone_number = models.CharField(max_length=15)
#     email = models.EmailField()
#     branch = models.CharField(max_length=50)
#     college_regd = models.CharField(max_length=20, unique=True)  # Primary key for search
#     roll = models.CharField(max_length=20)
#     address = models.TextField()
#     attendance_total = models.IntegerField(default=0)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} ({self.college_regd})"

# class AttendanceRecord(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     date = models.DateField()
#     present = models.BooleanField(default=False)

#     class Meta:
#         unique_together = ('student', 'date')  # One record per student per day




# clsbook/models.py
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password


class ClassBook(models.Model):
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    teacher_name = models.CharField(max_length=100)
    teacher_email = models.EmailField(default='')  # ✅ NEW FIELD
    password_hash = models.CharField(max_length=128)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='classbooks',
        null=True  # Temporarily allow null for existing records
    )  # ✅ NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # ✅ NEW FIELD
    updated_at = models.DateTimeField(auto_now=True, null=True)  # ✅ NEW FIELD

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return f"{self.class_name} - {self.section} ({self.teacher_name})"

    class Meta:
        ordering = ['-created_at']
        # Ensure unique class-section per user
        unique_together = ['class_name', 'section', 'created_by']


class Student(models.Model):
    class_book = models.ForeignKey(ClassBook, on_delete=models.CASCADE, related_name='students')
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    branch = models.CharField(max_length=50)
    college_regd = models.CharField(max_length=20, unique=True)
    roll = models.CharField(max_length=20)
    address = models.TextField()
    attendance_total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.college_regd})"


class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'date')
