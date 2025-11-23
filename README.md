# 🗂️ KannMind Backend

A modern Kanban board backend built with **Django** and **Django REST Framework**.  
Provides a full-featured REST API for managing boards, lists (columns), and tasks (cards).  
Designed to be used with any frontend (React, Vue, Angular, Flutter, etc.).

---

## 🚀 Features
- 🔐 User registration & token-based authentication
- 📋 CRUD operations for:
  - Boards
  - Lists (Columns)
  - Tasks (Cards)
- 👥 Permission system for shared/private boards
- 🧩 RESTful API structure designed for frontend integration
- 🛠️ Admin panel for database management

---

## ⚙️ Tech Stack
| Component | Version / Tool |
|----------|----------------|
| Language | Python 3.x |
| Framework | Django 4.x+ |
| API Toolkit | Django REST Framework |
| Database | SQLite / PostgreSQL (configurable) |
| Auth System | Token Authentication (optional JWT support) |

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/philiptesch/kanmind_app_backend
```

### 2️⃣ Create and activate a virtual environment
### Windows (PowerShell)
```bash
python -m venv env
.\env\Scripts\Activate.ps1   
```
### Windows (CMD)
```bash
python -m venv env
env\Scripts\activate.bat 
```
### macOS / Linux
```bash
python3 -m venv env
source env/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Apply database migrations
1 Makemigrations for each app (creates migration files from models):
```bash
python manage.py makemigrations python manage.py
makemigrations kanmind_board_app # separate for Board/Task/Comment models
```
2 Migrate (applies the migrations to the database):
```bash
python manage.py migrate
```
Note: If you add new models in any app, always run makemigrations APP_NAME first, otherwise the tables won’t be created.

### 5️⃣ Create a superuser (admin account)

```bash
python manage.py createsuperuser
```

### 6️⃣ Run the development server
```bash
python manage.py runserver
```

📍 API Endpoint: http://127.0.0.1:8000/  
📍 Admin Panel: http://127.0.0.1:8000/admin/



## 📖 API Overview

The backend provides endpoints for managing:

- 🧩 Boards
- 🗂️ Tasks
- 💬 Comments
- 👤 User Authentication (Register/Login)

Use tools like **Postman** or your frontend to interact with the API.

### 🔐 Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/registration/` | Register a new user |
| POST | `/api/login/` | Log in and retrieve token |
| GET | `/api/email-check/` | Check if an email is already in use |

### 🗂️ Board Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/boards/` | List all boards |
| POST | `/api/boards/` | Create a new board |
| GET | `/api/boards/{board_id}/` | Retrieve a board |
| PATCH | `/api/boards/{board_id}/` | Update a board |
| DELETE | `/api/boards/{board_id}/` | Delete a board |

### 📋 Task Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks/assigned-to-me/` | Get tasks assigned to user |
| GET | `/api/tasks/reviewing/` | Get tasks user reviews |
| POST | `/api/tasks/` | Create a new task |
| PATCH | `/api/tasks/{task_id}/` | Update a task |
| DELETE | `/api/tasks/{task_id}/` | Delete a task |
| GET | `/api/tasks/{task_id}/comments/` | List comments for a task |
| POST | `/api/tasks/{task_id}/comments/` | Add comment to a task |
| DELETE | `/api/tasks/{task_id}/comments/{comment_id}/` | Remove a comment |

---

## 📂 Project Structure (Overview)
```
KannMind_Backend/
├── kannmind/        # Core application
│   ├── models.py    # Data models (Board, Task, etc.)
│   ├── views.py     # API views
│   ├── serializers.py # DRF serializers
│   └── urls.py      # API routing
├── manage.py
├── requirements.txt
└── README.md        # Project documentation
```

---

## 🤝 Contributing
Contributions are welcome!  
If you'd like to improve this project, open an issue or submit a pull request.

---

## 📄 License
MIT License © philiptesch
