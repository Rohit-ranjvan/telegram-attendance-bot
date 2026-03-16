import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    os.getenv("GOOGLE_CREDENTIALS_FILE"), scope
)

client = gspread.authorize(creds)

sheet = client.open("Attendance_System")

students_sheet = sheet.worksheet("students")
batch_sheet = sheet.worksheet("batches")
faculty_sheet = sheet.worksheet("faculty")
attendance_sheet = sheet.worksheet("attendance")