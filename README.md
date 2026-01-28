<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=MindHook&fontSize=60&desc=Social%20Engineering%20Stimulator">
</p>

![Python](https://img.shields.io/badge/Python-3.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

# MindHook-Social-Engineering-Stimulator-

SeSim (Social Engineering Simulator) is a cybersecurity training and awareness platform designed to simulate real-world phishing and smishing attacks in a controlled and ethical environment.

It helps students, security teams, and researchers understand human-centric attack vectors and analyze user behavior against social engineering techniques.

---

## 🚀 Features

### 📧 Phishing Simulation
- Custom phishing emails using Quill.js editor
- Predefined templates (Google & Microsoft style)
- HTML email rendering with realistic layouts

### 📱 Smishing Simulation
- SMS-based phishing (smishing) simulation
- Separate interface and logs

### 🖥️ Fake Login Pages
- Google-style phishing login pages
- CSS + JavaScript powered UI
- Secure data logging (for educational analysis only)

### 📊 Logging & Analysis
- Separate logs for phishing and smishing
- Timestamped victim interactions
- Web-based log viewer

### 🔐 Secure Backend
- FastAPI-based backend
- Input validation & OWASP-aware design
- No real credential misuse

---

## 🛠️ Technology Stack

### Backend
- Python 3.x
- FastAPI
- Jinja2 Templates
- SMTP (Email simulation)
- Uvicorn

### Frontend
- HTML5
- Tailwind CSS
- JavaScript
- Quill.js (WYSIWYG editor)

### Security
- OWASP Top 10 considerations
- Secure routing and input handling

---

## 📂 Project Structure

```
SeSim/
│
├── templates/
│ ├── phishing_form.html
│ ├── smishing_form.html
│ ├── fake_google_login.html
│ └── logs.html
│
├── static/
│ ├── css/
│ ├── js/
│ └── images/
|
├── ScreenShot
|
├── main.py
├── mailer.py
├── smishr.py
├── viewlogs.py
├── db.py
├── mindhook-logo.png
├── pixel.png
├── INSTALL.md
├── CONTRIBUTING.md
├── LICENSE
├── SECURITY.md
├── CODE_OF_CONDUCT.md
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

📌 **Detailed installation steps are available here:**  
👉 [`INSTALL.md`](INSTALL.md)

---

## 🎯 Use Cases
- Cybersecurity awareness training  
- Ethical hacking labs  
- Social engineering research  
- Academic projects  
- Blue team behavior analysis  

---

## ⚠️ Disclaimer

This project is strictly for educational and ethical purposes only.  
The author is not responsible for any misuse of this tool.

---

## 🤝 Contribution

Contributions are welcome!  
Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting a pull request.

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👤 Author

**Prateek Dangi**  
