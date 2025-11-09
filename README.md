
# 🗂️ Secure File Organizer & Encryption System

## 🔐 Overview

The **Secure File Organizer** is a Django-based web application that allows users to **upload, organize, encrypt, decrypt, and scan files** safely.  
It ensures every uploaded file is stored in a well-organized folder structure and secured using **AES encryption (via Cryptography-Fernet)**.  

Users can also monitor their activity history — every action (upload, encryption, decryption, deletion) is logged automatically.

---

## 🚀 Features

✅ **User Authentication**  
✅ **Smart File Organization**  
✅ **File Encryption / Decryption**  
✅ **Malware Scanning (Optional)**  
✅ **Activity Logs**  
✅ **Secure Folder System**

---

## 🧠 Project Architecture

```
file_org_django/
│
├── dashboard/
│   ├── migrations/
│   ├── templates/
│   │   └── dashboard/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       ├── upload.html
│   │       ├── login.html
│   │       └── register.html
│   ├── utils/
│   │   ├── security_utils.py
│   │   ├── file_utils.py
│   │   └── log_utils.py
│   ├── models.py
│   ├── forms.py
│   ├── urls.py
│   └── views.py
│
├── media/
│   ├── uploads/
│   ├── encrypted/
│   └── decrypted/
│
├── file_org_django/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── db.sqlite3
├── manage.py
└── README.md
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/file_org_django.git
cd file_org_django
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv .env
.env\Scripts\activate  # Windows
source .env/bin/activate # Linux/Mac
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a Superuser
```bash
python manage.py createsuperuser
```

### 6️⃣ Run the Server
```bash
python manage.py runserver
```

Then open the app in your browser:  
👉 **http://127.0.0.1:8000/**

---

## 🧩 Core Modules & Their Purpose

| Module | Description |
|--------|--------------|
| `views.py` | Handles user actions like upload, encrypt, decrypt |
| `models.py` | Defines database models |
| `security_utils.py` | Encrypts & decrypts files |
| `file_utils.py` | Organizes uploaded files |
| `log_utils.py` | Adds logs to the database |
| `forms.py` | Manages upload and registration forms |

---

## 🧰 Technologies Used

| Category | Technology |
|-----------|-------------|
| **Frontend** | HTML5, CSS3, Bootstrap |
| **Backend** | Django |
| **Database** | SQLite |
| **Security** | cryptography.fernet |
| **Environment** | Python 3.12 / Django 5.x |

---

## 🧠 Common HR Questions

**Q1. Why did you choose Django?**  
> Django provides built-in security, authentication, ORM, and admin panel which helps in rapid development.

**Q2. What is Fernet encryption?**  
> Fernet uses AES encryption and ensures data integrity with HMAC. It is symmetric, meaning the same key is used for encrypting and decrypting.

**Q3. How do you handle data security?**  
> All files are encrypted, user actions logged, and passwords stored as hashes by Django.

---

## 👨‍💻 Author

**Developed by:** Subash (Python Developer Intern – Zaalima Development)

---

## 🏁 License
This project is licensed under the MIT License.
