from sheets import students_sheet, faculty_sheet, batch_sheet, attendance_sheet
from datetime import datetime


def add_student(name, batch):
    students_sheet.append_row([name, batch])


def add_faculty(name):
    faculty_sheet.append_row([name])


def add_batch(batch, time, faculty):
    batch_sheet.append_row([batch, time, faculty])


def mark_attendance(batch, time, faculty, student, status):
    date = datetime.now().strftime("%Y-%m-%d")
    attendance_sheet.append_row([date, batch, time, faculty, student, status])