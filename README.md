# 📊 Telegram Attendance Bot

A **Telegram-based Attendance Management System** built using Python and Google Sheets.
This bot helps institutes manage batches, students, faculty, and attendance in a **simple, automated, and scalable way**.

---

## 🚀 Features

### 👨‍🏫 Management

* Add Faculty (`/addfaculty`)
* Add Batch (`/addbatch`)
* Add Students (`/addstudent`)

### 📅 Attendance System

* Mark attendance using `/mark`
* Select:

  * Batch → Time → Faculty → Students
* Mark **Present / Absent**
* Auto-save in Google Sheets

### ⚡ Smart Features

* Auto attendance (mark all students in one screen)
* Batch completion (`/completebatch`)
* Completed batches are hidden automatically

### 📊 Reports

* `/todayattendance` → Today's attendance summary
* `/absentstudents` → List of absent students
* `/attendance_report` → Monthly student-wise report
* Batch-wise report system (professional level)

---

## 🏗️ Tech Stack

* **Python**
* **python-telegram-bot**
* **Google Sheets API (gspread)**
* **OAuth2 Credentials**

---

## 📁 Project Structure

```
project/
│
├── app.py              # Main bot logic
├── database.py         # Data handling (Sheets logic)
├── sheets.py           # Google Sheets connection
├── requirements.txt
├── .env                # Environment variables (not pushed)
├── credentials.json    # Google API key (not pushed)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```
git clone https://github.com/Rohit-ranjvan/telegram-attendance-bot.git
cd telegram-attendance-bot
```

---

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 3️⃣ Setup Environment Variables

Create `.env` file:

```
BOT_TOKEN=your_telegram_bot_token
GOOGLE_CREDENTIALS_FILE=credentials.json
```

---

### 4️⃣ Google Sheets Setup

Create a Google Sheet named:

```
Attendance_System
```

### Required Sheets:

#### 1. students

```
student_name | batch_name
```

#### 2. batches

```
batch_name | batch_time | faculty_name | status
```

#### 3. faculty

```
faculty_name
```

#### 4. attendance

```
date | batch | time | faculty | student | status
```

---

### 5️⃣ Run the Bot

```
python app.py
```

---

## 🔐 Security

* `.env` and `credentials.json` are **excluded using `.gitignore`**
* Never expose API keys or tokens publicly
* Use environment variables for all secrets

---

## 📌 Commands List

| Command              | Description             |
| -------------------- | ----------------------- |
| `/addfaculty`        | Add new faculty         |
| `/addbatch`          | Add new batch           |
| `/addstudent`        | Add student             |
| `/mark`              | Start attendance        |
| `/completebatch`     | Mark batch completed    |
| `/todayattendance`   | View today’s attendance |
| `/absentstudents`    | View absent students    |
| `/attendance_report` | Monthly report          |

## 👨‍💻 Author

**Rohit Ranjvan**

---

## ⭐ Support

If you like this project:

* Star ⭐ the repo
* Share it
* Contribute 🚀
