# from django.shortcuts import render

# # Create your views here.
# def studentviewer(request):
#     return render(request ,"studentviewer/studentviewerhome.html")

# studentviewer/views.py
# from django.shortcuts import render
# from clsbook.models import ClassBook, Student

# def studentviewer(request):
#     classbooks = ClassBook.objects.all()
#     selected_class = request.GET.get('classbook')
#     students = Student.objects.all()

#     if selected_class:
#         students = students.filter(class_book_id=selected_class)

#     return render(request, 'studentviewer/studentviewerhome.html', {
#         'classbooks': classbooks,
#         'students': students,
#         'selected_class': selected_class,
#     })


# studentviewer/views.py
from django.shortcuts import render
from django.db.models import Count, Sum
from clsbook.models import ClassBook, Student, AttendanceRecord
from django.utils import timezone

def studentviewer(request):
    classbooks = ClassBook.objects.all()
    selected_class_id = request.GET.get('classbook')
    section_filter = request.GET.get('section')

    students = Student.objects.all()

    if selected_class_id:
        students = students.filter(class_book_id=selected_class_id)
        selected_class = ClassBook.objects.get(id=selected_class_id)
    else:
        selected_class = None

    if section_filter:
        students = students.filter(class_book__section=section_filter)

    # Calculate stats
    total_students = Student.objects.count()
    today = timezone.now().date()
    total_present_today = AttendanceRecord.objects.filter(date=today, present=True).count()

    # Add percentage to each student
    for s in students:
        if s.attendance_total > 0:
            # Simple percentage (you can improve with total classes taken)
            s.attendance_percentage = (s.attendance_total / max(1, AttendanceRecord.objects.filter(student=s).count())) * 100
        else:
            s.attendance_percentage = 0

    # Get unique sections for filter
    all_sections = ClassBook.objects.values_list('section', flat=True).distinct()

    return render(request, 'studentviewer/studentviewerhome.html', {
        'classbooks': classbooks,
        'students': students,
        'selected_class': selected_class,
        'total_students': total_students,
        'total_present_today': total_present_today,
        'all_sections': all_sections,
    })