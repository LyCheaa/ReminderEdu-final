# ReminderEDU 2.0

A comprehensive educational reminder and task management application designed to help students stay organized and never miss important deadlines, assignments, and study sessions.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### Core Functionality
- **Smart Reminders**: Set customizable reminders for assignments, exams, and important dates
- **Task Management**: Create, organize, and track academic tasks with priorities
- **Due Date Tracking**: Never miss a deadline with automatic alerts and notifications
- **Category Organization**: Sort reminders by subject, class, or custom categories
- **Progress Monitoring**: Track completion status of assignments and study goals

### User Experience
- **Intuitive Interface**: Clean, user-friendly web interface for easy navigation
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Quick Add**: Rapidly add reminders without complex forms
- **Color-Coded System**: Visual organization of tasks by priority or category
- **Search & Filter**: Quickly find specific reminders and tasks

### Academic Focus
- **Class-Based Organization**: Organize reminders by courses and subjects
- **Study Schedule Planning**: Plan study sessions and review periods
- **Assignment Tracking**: Monitor assignment status from creation to completion
- **Exam Preparation**: Set reminders for exam dates and study milestones

## 🛠 Tech Stack

| Technology | Purpose | Percentage |
|-----------|---------|-----------|
| **Python** | Backend logic, server-side processing | 66.1% |
| **HTML** | Frontend structure, web interface | 33.9% |

### Backend (Python)
- Flask/Django framework for web server
- Database management and data persistence
- Business logic and reminder processing
- API endpoints for frontend communication

### Frontend (HTML)
- Responsive web pages
- Interactive forms and UI components
- Client-side validation
- Integration with backend via JavaScript

## 📁 Project Structure

```
ReminderEDU-2-/
├── README.md
├── requirements.txt          # Python dependencies
├── app.py                    # Main application file
├── config.py                 # Configuration settings
│
├── app/
│   ├── __init__.py
│   ├── models/               # Data models
│   │   ├── reminder.py
│   │   ├── task.py
│   │   └── user.py
│   ├── routes/               # API routes and endpoints
│   │   ├── reminders.py
│   │   ├── tasks.py
│   │   └── auth.py
│   ├── utils/                # Utility functions
│   │   ├── validators.py
│   │   └── helpers.py
│   └── services/             # Business logic
│       ├── reminder_service.py
│       └── notification_service.py
│
├── templates/                # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── reminders.html
│   ├── tasks.html
│   └── settings.html
│
├── static/                   # Static files
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│
└── tests/                    # Unit and integration tests
    ├── test_models.py
    ├── test_routes.py
    └── test_services.py
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/LyCheaa/ReminderEDU-2-.git
   cd ReminderEDU-2-
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**
   - Copy `config.py.example` to `config.py` (if applicable)
   - Update configuration settings as needed

5. **Initialize the database**
   ```bash
   python manage.py db init
   python manage.py db migrate
   python manage.py db upgrade
   ```

6. **Run the application**
   ```bash
   python app.py
   ```
   
   The application will be available at `http://localhost:5000`

## 💻 Usage

### Getting Started

1. **Create an Account**: Sign up with your email and create a password
2. **Set Up Classes**: Add your courses/classes for the semester
3. **Add Reminders**: Start creating reminders for assignments and exams
4. **Configure Notifications**: Choose how and when you want to receive alerts

### Creating a Reminder

1. Navigate to the "New Reminder" section
2. Fill in the following information:
   - **Title**: Assignment or event name
   - **Subject/Class**: Select the relevant class
   - **Due Date**: Set the date and time
   - **Priority**: Choose Low, Medium, or High
   - **Description**: Add additional details (optional)
   - **Notification**: Set when you want to be reminded

3. Click "Create Reminder"

### Managing Tasks

- **View All Tasks**: See your complete task list in the dashboard
- **Filter Tasks**: Filter by subject, priority, or due date
- **Update Status**: Mark tasks as In Progress, Completed, or Overdue
- **Edit/Delete**: Modify or remove tasks as needed

### Dashboard Features

- **Quick Overview**: See today's and upcoming deadlines
- **Statistics**: View task completion rates and productivity metrics
- **Calendar View**: Visual representation of due dates and events
- **Recent Activity**: Track recently added or updated reminders

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/ReminderEDU-2-.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow PEP 8 style guide for Python code
   - Add comments and docstrings
   - Update tests as needed

4. **Commit your changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```

5. **Push to the branch**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Support

For support, issues, or feature requests, please:
- Open an issue on GitHub
- Contact the development team
- Check existing documentation and FAQs

## 🎯 Future Enhancements

- [ ] Mobile app (iOS/Android)
- [ ] Integration with calendar services (Google Calendar, Outlook)
- [ ] Collaborative reminders for group projects
- [ ] AI-powered study recommendations
- [ ] Export reminders to PDF
- [ ] Dark mode theme
- [ ] Multi-language support

---

**Made with ❤️ for students everywhere**

Last Updated: May 2026
