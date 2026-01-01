# from django.shortcuts import render

# # Create your views here.
# def stdadd(request):
#     return render(request ,"stdadd/stdadder.html")

# stdadd/views.py
# stdadd/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from clsbook.models import ClassBook, Student, AttendanceRecord
from clsbook.forms import StudentForm


def stdadd(request):
    classbooks = ClassBook.objects.all()
    selected = None
    students = []
    today = timezone.now().date()

    # Get selected classbook from dropdown
    classbook_id = request.GET.get('classbook')
    if classbook_id:
        selected = get_object_or_404(ClassBook, id=classbook_id)
        students = selected.students.all()

        # Pre-compute today's attendance for checkboxes
        for student in students:
            student.is_present_today = AttendanceRecord.objects.filter(
                student=student, date=today, present=True
            ).exists()

        # Password protection
        session_classbook_id = request.session.get('classbook_id')
        if session_classbook_id != selected.id:
            if request.method == 'POST' and 'password' in request.POST:
                if selected.check_password(request.POST['password']):
                    request.session['classbook_id'] = selected.id
                    messages.success(request, 'Access granted!')
                else:
                    messages.error(request, 'Wrong password!')
                    return redirect('stdadd:password_prompt')
            else:
                # Show password prompt
                return render(request, 'stdadd/password_prompt.html', {'classbook': selected})

        # Handle Add Student
        if request.method == 'POST' and 'add_student' in request.POST:
            form = StudentForm(request.POST)
            if form.is_valid():
                student = form.save(commit=False)
                student.class_book = selected
                student.save()
                messages.success(request, f'Student {student.first_name} {student.last_name} added!')
                return redirect(request.path + f'?classbook={selected.id}')
        else:
            form = StudentForm()

        # Handle Attendance Submission
        if request.method == 'POST' and 'attendance' in request.POST:
            present_count = 0
            for student in students:
                is_present = request.POST.get(f'att_{student.id}') == 'on'
                AttendanceRecord.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={'present': is_present}
                )
                if is_present and not student.is_present_today:  # Only increment if newly marked present
                    student.attendance_total += 1
                    student.save()
                    present_count += 1
            messages.success(request, f'Attendance submitted for {today}! ({present_count} present)')
            return redirect(request.path + f'?classbook={selected.id}')

    else:
        # No class selected
        form = StudentForm()

    return render(request, 'stdadd/stdadder.html', {
        'classbooks': classbooks,
        'selected': selected,
        'students': students,
        'today': today,
        'student_form': StudentForm() if 'selected' not in locals() or not selected else StudentForm(),
    })


# # Optional: Keep reset_password if you want teacher to reset from here
# # Or remove if it's only in clsbook app
# def reset_password(request, pk):
#     classbook = get_object_or_404(ClassBook, pk=pk)
#     if request.method == 'POST':
#         new_pass = request.POST.get('new_password')
#         confirm_pass = request.POST.get('confirm_password')
#         if new_pass and new_pass == confirm_pass:
#             classbook.set_password(new_pass)
#             classbook.save()
#             messages.success(request, 'Password reset successfully!')
#         else:
#             messages.error(request, 'Passwords do not match or are empty.')
#         return redirect('clsbook:home')
#     return render(request, 'clsbook/reset_password.html', {'classbook': classbook})



# def stdadd(request):
#     classbooks = ClassBook.objects.all()
#     selected = None
#     students = []
#     today = timezone.now().date()

#     classbook_id = request.GET.get('classbook')
#     if classbook_id:
#         selected = get_object_or_404(ClassBook, id=classbook_id)
#         students = selected.students.all()

#         # Pre-compute today's attendance
#         for student in students:
#             student.is_present_today = AttendanceRecord.objects.filter(
#                 student=student, date=today, present=True
#             ).exists()

#         # Always ask for password — no session storage
#         if request.method == 'POST' and 'password' in request.POST:
#             if selected.check_password(request.POST['password']):
#                 # Password correct → show management page
#                 pass  # continue below
#             else:
#                 messages.error(request, 'Incorrect password!')
#                 return render(request, 'stdadd/password_prompt.html', {'classbook': selected})
#         else:
#             # First visit or back button → show password prompt
#             return render(request, 'stdadd/password_prompt.html', {'classbook': selected})

#         # === Below this line: only runs after correct password ===

#         # Add Student
#         if request.method == 'POST' and 'add_student' in request.POST:
#             form = StudentForm(request.POST)
#             if form.is_valid():
#                 student = form.save(commit=False)
#                 student.class_book = selected
#                 student.save()
#                 messages.success(request, f'Student {student.first_name} added!')
#                 return redirect(f'/stdadd/?classbook={selected.id}')

#         # Attendance Submit
#         if request.method == 'POST' and 'attendance' in request.POST:
#             present_count = 0
#             for student in students:
#                 is_present = request.POST.get(f'att_{student.id}') == 'on'
#                 record, created = AttendanceRecord.objects.update_or_create(
#                     student=student, date=today, defaults={'present': is_present}
#                 )
#                 if is_present and not student.is_present_today:
#                     student.attendance_total += 1
#                     student.save()
#                     present_count += 1
#             messages.success(request, f'Attendance submitted! ({present_count} present)')
#             return redirect(f'/stdadd/?classbook={selected.id}')

#     return render(request, 'stdadd/stdadder.html', {
#         'classbooks': classbooks,
#         'selected': selected,
#         'students': students or [],
#         'today': today,
#         'student_form': StudentForm(),
#     })

def password_prompt(request):
    return render(request ,"stdadd/password_prompt")
