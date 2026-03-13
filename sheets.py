import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)

sheet = client.open("Attendance_System")

students_sheet = sheet.worksheet("students")
batch_sheet = sheet.worksheet("batches")
faculty_sheet = sheet.worksheet("faculty")
attendance_sheet = sheet.worksheet("attendance")