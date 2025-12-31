from django.contrib import admin
from allauth.account.admin import EmailAddressAdmin
from allauth.account.models import EmailAddress
from .models import ClassBook, Student, AttendanceRecord

# Register your models here.
admin.site.register(ClassBook)
admin.site.register(Student)
admin.site.register(AttendanceRecord)

admin.site.unregister(EmailAddress)
admin.site.register(EmailAddress, EmailAddressAdmin)
