from sheets import students_sheet, batch_sheet, faculty_sheet, attendance_sheet
from datetime import datetime


# -------------------------
# FACULTY
# -------------------------

def add_faculty(name):
    faculty_sheet.append_row([name])


# -------------------------
# BATCH
# -------------------------

def add_batch(batch, time, faculty):
    # Added status column (IMPORTANT FIX)
    batch_sheet.append_row([batch, time, faculty, "Active"])


def get_batches():

    data = batch_sheet.get_all_records()

    batches = []

    for d in data:

        # Safe status handling (handles wrong column names also)
        status = (
            d.get("status")
            or d.get("Status")
            or "Active"
        )

        if str(status).strip().lower() == "active":
            batches.append(d["batch_name"])

    return list(set(batches))


# alias used by app.py
def get_batch_timings(batch):

    data = batch_sheet.get_all_records()

    times = []

    for d in data:

        status = (
            d.get("status")
            or d.get("Status")
            or "Active"
        )

        if (
            d["batch_name"] == batch and
            str(status).strip().lower() == "active"
        ):
            times.append(d["batch_time"])

    return list(set(times))


def get_times(batch):

    data = batch_sheet.get_all_records()

    times = []

    for d in data:

        status = (
            d.get("status")
            or d.get("Status")
            or "Active"
        )

        if (
            d["batch_name"] == batch and
            str(status).strip().lower() == "active"
        ):
            times.append(d["batch_time"])

    return list(set(times))


def get_faculty(batch, time):

    data = batch_sheet.get_all_records()

    return [
        d["faculty_name"]
        for d in data
        if d["batch_name"] == batch and d["batch_time"] == time
    ]


# -------------------------
# STUDENTS
# -------------------------

def add_student(name, batch):
    students_sheet.append_row([name, batch])


def get_students(batch):

    data = students_sheet.get_all_records()

    return [
        d["student_name"]
        for d in data
        if d["batch_name"] == batch
    ]


# -------------------------
# ATTENDANCE
# -------------------------

def save_attendance(batch, time, faculty, student, status):

    date = datetime.now().strftime("%Y-%m-%d")

    attendance_sheet.append_row([
        date,
        batch,
        time,
        faculty,
        student,
        status
    ])


# wrapper used by bot logic
def save_attendance_simple(student, batch, time, status):

    faculty_list = get_faculty(batch, time)

    faculty = faculty_list[0] if faculty_list else ""

    save_attendance(batch, time, faculty, student, status)


# -------------------------
# TODAY ATTENDANCE
# -------------------------

def get_today_attendance():

    today = datetime.now().strftime("%Y-%m-%d")

    data = attendance_sheet.get_all_records()

    return [
        r for r in data
        if r["date"] == today
    ]


# -------------------------
# ABSENT STUDENTS
# -------------------------

def get_absent_students():

    today = datetime.now().strftime("%Y-%m-%d")

    data = attendance_sheet.get_all_records()

    return [
        r["student"]
        for r in data
        if r["date"] == today and r["status"] == "Absent"
    ]


# -------------------------
# MONTHLY REPORT
# -------------------------

def get_batch_report(batch):

    data = attendance_sheet.get_all_records()

    month = datetime.now().strftime("%Y-%m")

    rows = [
        r for r in data
        if r["batch"] == batch and r["date"].startswith(month)
    ]

    report = {}

    for r in rows:

        student = r["student"]

        if student not in report:
            report[student] = {
                "present": 0,
                "total": 0
            }

        report[student]["total"] += 1

        if r["status"] == "Present":
            report[student]["present"] += 1

    return report


# -------------------------
# BATCH EXISTS
# -------------------------

def batch_exists(batch, time, faculty):

    data = batch_sheet.get_all_records()

    for row in data:
        if (
            row["batch_name"] == batch and
            row["batch_time"] == time and
            row["faculty_name"] == faculty
        ):
            return True

    return False


# -------------------------
# COMPLETE BATCH
# -------------------------

def complete_batch(batch, time):

    data = batch_sheet.get_all_records()

    for i, row in enumerate(data, start=2):

        if row["batch_name"] == batch and row["batch_time"] == time:
            # Column 4 = status
            batch_sheet.update_cell(i, 4, "Completed")
            return True

    return False