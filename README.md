# 🔐 SecureShare – Encrypted File Sharing System

SecureShare is a cybersecurity-focused web application built with **Python Flask** that allows users to securely upload, store, and download files using strong cryptography and access control mechanisms.

The system ensures that files are never stored or transferred in plaintext and can only be accessed by the authorized owner.

---

## 🎯 Objective

To design and implement a secure file sharing platform that demonstrates:

* Encryption at rest
* Secure key exchange
* Authenticated access control
* Protected file transfer

---

## 🛠 Tech Stack

* **Backend:** Python (Flask)
* **Database:** SQLite (SQLAlchemy ORM)
* **Authentication:** Flask-Login
* **Cryptography:** PyCryptodome
* **Hashing:** Werkzeug Security
* **Token Security:** Itsdangerous (signed timed URLs)
* **Frontend:** HTML (Jinja Templates)

---

## 🔒 Security Features

### 1. User Authentication

* Users register and login using hashed passwords
* Passwords stored using secure hashing (no plaintext storage)

### 2. AES File Encryption

* Every uploaded file is encrypted before storage
* Prevents data exposure if storage is compromised

### 3. RSA Key Protection

* Each user gets a unique RSA key pair
* AES encryption key is encrypted using the user's public key
* Only the owner can decrypt the file

### 4. Secure Download Links (Zero-Trust Access)

* Download links expire after **60 seconds**
* Links cannot be reused or shared
* Prevents replay attacks and unauthorized access

### 5. Access Control

* Only the file owner can download their files
* Token verification + user verification required

---

## 📂 System Workflow

1. User logs in
2. Uploads file
3. System encrypts file using AES
4. AES key encrypted using RSA public key
5. Encrypted file stored on server
6. User requests download
7. Temporary signed token generated
8. Token validated + ownership checked
9. File decrypted and sent to user

---

## ▶️ How to Run

### 1. Install dependencies

```bash
pip install flask flask-login flask-sqlalchemy pycryptodome itsdangerous
```

### 2. Run application

```bash
python app.py
```

### 3. Open browser

```
http://127.0.0.1:5000
```

---

## 📌 Example Security Scenario

Even if someone:

* Steals the download URL
* Accesses the storage folder
* Intercepts traffic

They **still cannot read the file** because:

* File is AES encrypted
* Key is RSA protected
* Download token expires
* Ownership verification required

---

## 🎓 Learning Outcomes

This project demonstrates practical implementation of:

* Symmetric Encryption (AES)
* Asymmetric Encryption (RSA)
* Secure Key Exchange
* Authentication & Authorization
* Secure Session Transfer
* Replay Attack Prevention

---

## 👨‍💻 Author
DZODZODZI CEDRICK
Cybersecurity Internship Project – Secure File Sharing System
