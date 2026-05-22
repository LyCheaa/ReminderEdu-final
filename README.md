Application Description
Overview
ReminderEDU is an intelligent reminder and task management system designed specifically for educational purposes. It helps students, educators, and learners organize their tasks, manage deadlines, and stay productive with timely notifications and smart task prioritization.

What This Application Allows Users to Do:
•	Create & Manage Reminders: Easily add, edit, and delete academic reminders and assignments with detailed information
•	Schedule Tasks: Set specific due dates and times for assignments, projects, and study sessions
•	Subject Organization: Categorize reminders by subject (e.g., Math, Science, English, History, etc.)
•	Smart Notifications: Receive intelligent alerts based on urgency levels and time remaining
•	Deadline Tracking: View time remaining for each task with automated urgency categorization:
o	Overdue: Tasks past their due date
o	Due Soon!: Tasks due within the next hour
o	Today: Tasks due within 24 hours
o	Upcoming: Tasks due within 3 days
o	Planned: Tasks scheduled for later
•	Task Sorting: Automatically sort assignments by urgency to prioritize workload
•	Data Persistence: All reminders are automatically saved and loaded from persistent storage
•	User-Friendly Interface: Clean, intuitive, responsive web interface for easy task management
Assignment Details: Store and display assignment name, subject, due date, due time, and time remaining


OOP Concepts Used
ReminderEDU demonstrates several core Object-Oriented Programming principles:
1. Abstraction
•	Abstract Base Classes (ABC):
o	IInputSource - Abstract interface for input sources
o	IStorage - Abstract interface for data persistence
•	Hides implementation details while providing clear interfaces
2. Inheritance
•	Concrete Implementations:
o	ManualInputSource inherits from IInputSource
o	CsvStorage inherits from IStorage
•	Allows multiple input and storage strategies without changing core logic
3. Encapsulation
•	Private Attributes: Uses underscore prefix (_name, _subject, _due_datetime, _id)
•	Property Decorators: Implements getters and setters for controlled access:
•	@property
•	def name(self):
•	    return self._name
•	
•	@name.setter
•	def name (self, value):
    # Validation logic
•	Protects data integrity and allows validation
4. Polymorphism
•	Interface Implementation: Different input sources and storage mechanisms can be used interchangeably
•	ScheduleManager works with any IInputSource or IStorage implementation
•	Enables flexible architecture and easy extensibility
5. Composition
•	ScheduleManager contains a CsvStorage object
•	ManualInputSource contains form data
•	Objects are composed of other objects to build complex behavior
6. Single Responsibility Principle
•	Assignment - Represents a single task
•	ManualInputSource - Handles manual input
•	CsvStorage - Manages file I/O
•	ScheduleManager - Orchestrates operations


Technologies Used
Python- Backend logic, server, core functionality, and CLI
Flask - Lightweight web framework for routing and request handling
CSV - Data persistence and storage format
HTML - Structure and markup for web interface

ReminderEDU/
├── README.md                    # Project documentation
├── app.py                        # Flask application & routing
├── core_logic.py                 # Core business logic and data models
├── test_logic.py                 # Unit tests
├── requirements.txt              # Python dependencies
├── schedule.csv                  # Data storage (auto-generated)
├── static/                       # Static assets
│   ├── css/
│   │   └── style.css            # Application styling
│   └── js/
│       └── script.js             # Frontend JavaScript
└── templates/                    # HTML templates
    ├── base.html                # Base template with layout
    ├── index.html               # Main dashboard
    └── reminder_detail.html      # Individual reminder view


How to Run
Prerequisites
•	Python 3.7 or higher
•	pip (Python package manager)
•	A modern web browser (Chrome, Firefox, Safari, Edge)
•	Git (for cloning the repository)
Installation Steps
1. Clone the Repository
git clone https://github.com/LyCheaa/ReminderEDU.git
cd ReminderEDU
2. Create a Virtual Environment (Recommended)
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
If requirements.txt doesn't exist, install manually:
pip install flask pytest
4. Navigate to the Folder
cd ReminderEDU
Verify the following files are present:
•	app.py
•	core_logic.py
•	test_logic.py
•	templates/ directory
•	static/ directory
5. Run the Application
# Option 1: Direct Flask execution
python app.py

# Option 2: Using Flask CLI
flask run
You should see output similar to:
WARNING in app.run() This is a development server. Do not use it in production.
* Running on http://127.0.0.1:5000
* Debug mode: on

6. Access the Application
Open your web browser and navigate to:
http://localhost:5000

