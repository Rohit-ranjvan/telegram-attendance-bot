from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from database import add_student, add_faculty, add_batch, mark_attendance

TOKEN = "8622337889:AAEYP-YfmfzbMWHb3AAPDWpxLf6r28dohx4"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Attendance Bot Ready ✅")


async def addfaculty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.args[0]
    add_faculty(name)
    await update.message.reply_text("Faculty added")


async def addbatch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    batch = context.args[0]
    time = context.args[1]
    faculty = context.args[2]

    add_batch(batch, time, faculty)

    await update.message.reply_text("Batch created")


async def addstudent(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = context.args[0]
    batch = context.args[1]

    add_student(name, batch)

    await update.message.reply_text("Student added")


async def mark(update: Update, context: ContextTypes.DEFAULT_TYPE):

    batch = context.args[0]
    time = context.args[1]
    faculty = context.args[2]
    student = context.args[3]
    status = context.args[4]

    mark_attendance(batch, time, faculty, student, status)

    await update.message.reply_text("Attendance saved")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addfaculty", addfaculty))
app.add_handler(CommandHandler("addbatch", addbatch))
app.add_handler(CommandHandler("addstudent", addstudent))
app.add_handler(CommandHandler("mark", mark))

print("Bot running...")

app.run_polling()