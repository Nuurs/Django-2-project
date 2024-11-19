
from celery import shared_task
from django.core.mail import send_mail
from students.models import Student
from grades.models import Grade
from attendance.models import Attendance
from django.utils.timezone import now
import datetime

@shared_task
def send_daily_attendance_reminder():
    students = Student.objects.all()
    for student in students:
        send_mail(
            "Daily Attendance Reminder",
            "Dear {}, please mark your attendance for today.".format(student.name),
            "admin@school.com",
            [student.email],
        )

@shared_task
def send_grade_update_notification(student_id, course_name, grade):
    student = Student.objects.get(id=student_id)
    send_mail(
        "Grade Update Notification",
        "Dear {}, your grade for {} is updated to {}.".format(student.name, course_name, grade),
        "admin@school.com",
        [student.email],
    )

@shared_task
def send_daily_report():
    # Generate attendance and grades report for all students
    students = Student.objects.all()
    today = now().date()
    report = []
    for student in students:
        attendance = Attendance.objects.filter(student=student, date=today).values_list('status', flat=True)
        grades = Grade.objects.filter(student=student).values_list('course__name', 'grade')
        report.append(f"Student: {student.name}, Attendance: {list(attendance)}, Grades: {list(grades)}")
    
    # Email the report to the admin
    send_mail(
        "Daily Attendance and Grades Report",
        "\n".join(report),
        "admin@school.com",
        ["admin@school.com"],
    )

@shared_task
def send_weekly_performance_update():
    # Weekly summary email for each student
    students = Student.objects.all()
    for student in students:
        grades = Grade.objects.filter(student=student).values_list('course__name', 'grade')
        send_mail(
            "Weekly Performance Summary",
            f"Dear {student.name}, here is your performance summary:\n{list(grades)}",
            "admin@school.com",
            [student.email],
        )
