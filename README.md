# 🧠 AI-powered Applicant Tracking System (ATS)

An intelligent recruitment platform that leverages AI to streamline the hiring process—from job posting to candidate shortlisting. The system includes role-based access for admins, reviewers, and candidates, and uses AI to automatically evaluate resumes based on relevance to job descriptions.

---

## 🚀 Features

### 🔐 Role-Based Authentication
- **Admin**
  - Secure login
  - Post and manage job descriptions
- **Reviewer**
  - View candidate profiles and AI match scores
  - Shortlist or reject applications
- **Candidate**
  - Register and login
  - Apply to jobs with resume (PDF/DOC) and optional cover letter

### 🤖 AI Resume Screening
- Upon application submission:
  - The resume and job description are sent to an AI model
  - The model evaluates and returns a match score based on:
    - Skills
    - Experience
    - Relevance to the job
- Match score and candidate details are saved to the database

### 📊 Admin & Reviewer Dashboards
- Access and manage:
  - Candidate applications
  - AI-generated scores
  - Detailed profiles and uploaded resumes
  - Shortlist/Reject functionality

### 📧 Email Notifications
- Candidates receive automatic email updates when:
  - Shortlisted
  - Rejected

---

## 🛠️ Tech Stack (Example)

- **Frontend**: React / Vue / Angular
- **Backend**: Flask / Django / Node.js
- **AI Model**: BERT / spaCy / Custom NLP
- **Database**: PostgreSQL / MongoDB
- **Authentication**: JWT / OAuth
- **Email Service**: SendGrid / SMTP

---

## 📁 Suggested Project Structure

```
ats-ai/
│
├── backend/
│   ├── models/            # AI scoring, resume parsing logic
│   ├── routes/            # APIs for auth, jobs, applications
│   └── utils/             # Email service, document parsing
│
├── frontend/
│   ├── components/        # UI components
│   ├── pages/             # Login, dashboard, apply
│   └── services/          # API interactions
│
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ats-ai.git
cd ats-ai
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python app.py
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

---

## 📌 Future Enhancements

- Resume feedback and tips for candidates
- Admin analytics dashboard
- Interview scheduling
- Mobile responsive design

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to open a pull request or submit an issue.

---