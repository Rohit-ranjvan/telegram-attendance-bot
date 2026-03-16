import os
from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from database import *

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# ==========================
# START
# ==========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Attendance Bot Ready\n\n"
        "/addfaculty Name\n"
        "/addbatch Batch Time Faculty\n"
        "/addstudent Name Batch\n\n"
        "/showbatches\n"
        "/mark\n"
        "/completebatch Batch Time\n"
        "/todayattendance\n"
        "/absentstudents\n"
        "/attendance_report"
    )


# ==========================
# ADD FACULTY
# ==========================

async def addfaculty(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n/addfaculty FacultyName\n\nExample:\n/addfaculty Yogesh"
        )
        return

    name = " ".join(context.args)

    try:
        add_faculty(name)
        await update.message.reply_text(f"Faculty Added ✅\n\n{name}")
    except Exception as e:
        await update.message.reply_text("Error adding faculty ❌")
        print("Faculty Error:", e)


# ==========================
# ADD BATCH
# ==========================

async def addbatch(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 3:
        await update.message.reply_text(
            "Usage:\n/addbatch BatchName Time Faculty\n\nExample:\n/addbatch Python 4-6 Yogesh"
        )
        return

    batch = context.args[0]
    time = context.args[1]
    faculty = context.args[2]

    try:
        if batch_exists(batch, time, faculty):
            await update.message.reply_text(
                f"⚠ Batch already exists!\n\nBatch: {batch}\nTime: {time}\nFaculty: {faculty}"
            )
            return

        add_batch(batch, time, faculty)

        await update.message.reply_text(
            f"Batch Added Successfully ✅\n\nBatch: {batch}\nTime: {time}\nFaculty: {faculty}"
        )

    except Exception as e:
        await update.message.reply_text("Error adding batch ❌")
        print("Batch Error:", e)


# ==========================
# COMPLETE BATCH
# ==========================

async def completebatch(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/completebatch Batch Time\nExample:\n/completebatch Python 4-6"
        )
        return

    batch = context.args[0]
    time = context.args[1]

    try:
        if complete_batch(batch, time):
            await update.message.reply_text(
                f"✅ Batch Completed\n\nBatch: {batch}\nTime: {time}"
            )
        else:
            await update.message.reply_text("Batch not found ❌")

    except Exception as e:
        await update.message.reply_text("Error completing batch ❌")
        print("Complete Batch Error:", e)


# ==========================
# ADD STUDENT
# ==========================

async def addstudent(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage:\n/addstudent Name Batch\nExample:\n/addstudent Rohit Python"
        )
        return

    name = context.args[0]
    batch = " ".join(context.args[1:])

    try:
        add_student(name, batch)
        await update.message.reply_text(f"{name} added to {batch} ✅")
    except Exception as e:
        await update.message.reply_text("Error adding student ❌")
        print("Student Error:", e)


# ==========================
# SHOW BATCHES
# ==========================

async def showbatches(update: Update, context: ContextTypes.DEFAULT_TYPE):

    batches = get_batches()

    if not batches:
        await update.message.reply_text("No batches found")
        return

    text = "Batches\n\n"

    for b in batches:
        text += f"{b}\n"

    await update.message.reply_text(text)


# ==========================
# MARK ATTENDANCE
# ==========================

async def mark(update: Update, context: ContextTypes.DEFAULT_TYPE):

    batches = get_batches()

    if not batches:
        await update.message.reply_text("No active batches available ❌")
        return

    keyboard = [
        [InlineKeyboardButton(b, callback_data=f"batch|{b}")]
        for b in batches
    ]

    await update.message.reply_text(
        "📌 Select Batch",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def select_batch(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    batch = query.data.split("|")[1]

    timings = get_batch_timings(batch)

    if not timings:
        await query.edit_message_text("No active timings found ❌")
        return

    keyboard = [
        [InlineKeyboardButton(t, callback_data=f"time|{batch}|{t}")]
        for t in timings
    ]

    await query.edit_message_text(
        f"Batch: {batch}\nSelect Timing",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def select_time(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    _, batch, time = query.data.split("|")

    students = get_students(batch)

    if not students:
        await query.edit_message_text("No students found ❌")
        return

    context.user_data["batch"] = batch
    context.user_data["time"] = time

    attendance = {s: "Present" for s in students}
    context.user_data["attendance"] = attendance

    keyboard = []
    row = []

    for s in students:

        row.append(
            InlineKeyboardButton(f"{s} ✅", callback_data=f"toggle|{s}")
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton("💾 Save Attendance", callback_data="done")
    ])

    await query.edit_message_text(
        f"📋 Mark Attendance\nBatch: {batch}\nTime: {time}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def mark_attendance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    batch = context.user_data.get("batch")
    time = context.user_data.get("time")
    attendance = context.user_data.get("attendance")

    if data == "done":

        for student, status in attendance.items():
            save_attendance_simple(student, batch, time, status)

        await query.edit_message_text("✅ Attendance Saved Successfully")
        return

    student = data.split("|")[1]

    attendance[student] = (
        "Absent" if attendance[student] == "Present" else "Present"
    )

    keyboard = []
    row = []

    for s, status in attendance.items():

        icon = "✅" if status == "Present" else "❌"

        row.append(
            InlineKeyboardButton(f"{s} {icon}", callback_data=f"toggle|{s}")
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton("💾 Save Attendance", callback_data="done")
    ])

    await query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==========================
# REPORTS
# ==========================

async def todayattendance(update: Update, context: ContextTypes.DEFAULT_TYPE):

    rows = get_today_attendance()

    total = len(rows)
    present = len([r for r in rows if r["status"] == "Present"])
    absent = len([r for r in rows if r["status"] == "Absent"])

    await update.message.reply_text(
        f"Today's Attendance\n\nTotal: {total}\nPresent: {present}\nAbsent: {absent}"
    )


async def absentstudents(update: Update, context: ContextTypes.DEFAULT_TYPE):

    students = get_absent_students()

    if not students:
        await update.message.reply_text("All students present ✅")
        return

    text = "Absent Students\n\n" + "\n".join(students)

    await update.message.reply_text(text)


async def attendance_report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    batches = get_batches()

    if not batches:
        await update.message.reply_text("No active batches ❌")
        return

    keyboard = [
        [InlineKeyboardButton(b, callback_data=f"report|{b}")]
        for b in batches
    ]

    await update.message.reply_text(
        "Select Batch",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def batch_report(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    batch = query.data.split("|")[1]

    report = get_batch_report(batch)

    if not report:
        await query.edit_message_text("No data found")
        return

    text = f"📊 Attendance Report ({batch})\n\n"

    for student, stats in report.items():

        percent = round((stats["present"] / stats["total"]) * 100, 2)

        text += (
            f"{student}\n"
            f"✔ Present: {stats['present']}\n"
            f"📚 Total: {stats['total']}\n"
            f"📈 {percent}%\n\n"
        )

    await query.edit_message_text(text)


# ==========================
# APP SETUP
# ==========================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addfaculty", addfaculty))
app.add_handler(CommandHandler("addbatch", addbatch))
app.add_handler(CommandHandler("completebatch", completebatch))
app.add_handler(CommandHandler("addstudent", addstudent))
app.add_handler(CommandHandler("showbatches", showbatches))
app.add_handler(CommandHandler("mark", mark))
app.add_handler(CommandHandler("todayattendance", todayattendance))
app.add_handler(CommandHandler("absentstudents", absentstudents))
app.add_handler(CommandHandler("attendance_report", attendance_report))

app.add_handler(CallbackQueryHandler(select_batch, pattern="^batch"))
app.add_handler(CallbackQueryHandler(select_time, pattern="^time"))
app.add_handler(CallbackQueryHandler(mark_attendance, pattern="^(toggle|done)"))
app.add_handler(CallbackQueryHandler(batch_report, pattern="^report"))

print("Bot Running...")

app.run_polling()