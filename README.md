# SkillSphere

<p align="center">
  <strong>A collaborative platform for learning, building projects, discovering people, and sharing knowledge.</strong>
</p>

<p align="center">
  SkillSphere combines project management, social collaboration, intelligent discovery,
  activity tracking, feedback collection, and AI-powered recommendations in one platform.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.0-092E20?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Celery-5.x-37814A?logo=celery&logoColor=white" alt="Celery">
  <img src="https://img.shields.io/badge/Redis-Message%20Broker-DC382D?logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/Elasticsearch-8.x-005571?logo=elasticsearch&logoColor=white" alt="Elasticsearch">
  <img src="https://img.shields.io/badge/Tailwind%20CSS-Responsive%20UI-06B6D4?logo=tailwindcss&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/scikit--learn-AI%20Recommendations-F7931E?logo=scikitlearn&logoColor=white" alt="scikit-learn">
</p>

---

## Overview

**SkillSphere** is a full-stack learning and project collaboration platform built with Django.

The platform allows users to create and manage projects, collaborate with other members, upload files and folders, interact through comments and likes, follow other users, search for projects and people, receive notifications, and review their activity history.

SkillSphere also includes a content-based recommendation engine that analyzes user profiles and project content to recommend relevant open projects.

The project was developed collaboratively by a three-person team, with each member owning a distinct set of backend, frontend, infrastructure, and integration responsibilities.

---

## Core Features

### User Accounts and Profiles

- Custom Django user model
- Username and unique email authentication
- User biography and profile image
- Email verification workflow
- GitHub social authentication using `django-allauth`
- Profile editing
- Account deletion with confirmation
- Follow and unfollow system
- Follower and following relationships
- Public user profiles

### Project Management

- Create, view, edit, and delete projects
- Public and private project visibility
- Project statuses:
  - Open
  - In Progress
  - Completed
- Project ownership and membership
- Project tags
- Project views and download statistics
- Owner and collaborator access control
- Project invitations through secure invitation tokens
- Accept and decline invitation workflows

### Project Collaboration

- Join projects as collaborators
- Invite users through email
- Like and unlike projects
- Post project comments
- Share projects through:
  - Copyable links
  - Gmail compose
  - Application email
- Upload individual files
- Upload multiple files and folder structures
- Preserve uploaded relative paths
- GitHub-style project file display
- Download project files

### Dashboard

- Personalized project overview
- Owned and joined project summaries
- Recent platform activity
- Project and community statistics
- Responsive dashboard cards
- AI-powered project recommendations
- Dark mode support
- Mobile-friendly layouts

### Search and Discovery

- Search projects and users
- Elasticsearch-powered project indexing
- Search suggestions
- Search result filtering
- Project status filtering
- Search history
- Recent searches
- Paginated project and user results
- Highlighted search matches
- Explore page for public projects

### Notification System

- User-specific notifications
- Project notifications
- Comment notifications
- Invitation notifications
- Follow notifications
- Feedback-related notifications
- Read and unread notification states
- Notification dropdown and notification page
- Bulk mark-as-read actions

### Activity Tracking

- Central activity log model
- Login and logout tracking through Django signals
- Automatic logging of successful state-changing requests
- Request classification through a dedicated service layer
- Captured activity metadata:
  - User
  - Action type
  - Description
  - Request path
  - HTTP method
  - Response status
  - IP address
  - Timestamp
- Activity history page
- Activity pagination
- Database indexes for common activity queries
- Admin integration

Tracked actions include:

- Login and logout
- Project creation, editing, and deletion
- File uploads and downloads
- Project likes and comments
- Feedback submissions
- Profile changes
- Invitation management
- Account deletion

### Feedback System

- Submit structured platform feedback
- Feedback categories such as:
  - Suggestion
  - Bug report
  - Feature request
  - Compliment
- Feedback rating
- Feedback lifecycle statuses
- User feedback history
- Administrative review
- Admin response and reaction fields
- Feedback statistics
- Form validation
- Transaction-safe feedback creation
- Integration with the activity tracking system

### AI Project Recommendations

SkillSphere includes a content-based recommendation engine built with `scikit-learn`.

The system:

1. Builds a user profile document from the username and biography.
2. Builds project documents from project titles, descriptions, and tags.
3. Converts the documents into TF-IDF vectors.
4. Calculates similarity using cosine similarity.
5. Ranks the most relevant projects.
6. Returns a match score and an explanation.

Recommendation rules:

- Only public and open projects are considered.
- Projects owned by the user are excluded.
- Projects the user has already joined are excluded.
- A fallback strategy is used when profile information is incomplete.
- Recommendation errors do not prevent the dashboard from loading.

---

## Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python, Django |
| Database | PostgreSQL |
| Database Image | PostgreSQL 16 with pgvector support |
| Authentication | Django Authentication, django-allauth, GitHub OAuth |
| Asynchronous Tasks | Celery |
| Message Broker | Redis |
| Task Results | django-celery-results |
| Search | Elasticsearch, django-elasticsearch-dsl |
| AI Recommendation | scikit-learn, TF-IDF, cosine similarity |
| Frontend | Django Templates, Tailwind CSS |
| Icons | Lucide |
| Development Services | Docker, Docker Compose |
| Email | Django SMTP backend |

---

## Application Architecture

SkillSphere follows Django's modular application structure.

```text
SkillSphere/
├── activity_logs/     # Activity tracking, middleware, signals, services
├── dashboard/         # Dashboard views, data services, recommendation UI
├── feedback/          # Feedback forms, models, services, views, admin
├── notifications/     # Notification storage, views, and context processor
├── projects/          # Projects, files, invitations, likes, comments, tasks
├── search/            # Elasticsearch search, indexing, suggestions, history
├── skill_sphere/      # Global settings, URLs, Celery configuration
├── static/            # Shared CSS and JavaScript assets
├── templates/         # Shared base templates and layouts
├── theme/             # Tailwind CSS application
├── users/             # Authentication, profiles, following, verification
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

### Architectural Practices

- Separation of concerns through Django applications
- Service layers for reusable business logic
- Middleware for cross-cutting activity tracking
- Signals for authentication activity
- Celery tasks for background processing
- Elasticsearch document indexing
- Reusable template partials
- Environment-based database and email configuration
- Owner/member permission checks
- Graceful fallback behavior for optional intelligent features

---

## Team and Contributions

The following list describes the primary ownership of each team member. Integration, debugging, UI review, and merge conflict resolution were collaborative efforts.

### Person A — Nasim

GitHub: [@Soyokaze00](https://github.com/Soyokaze00)

**Primary responsibilities: Core platform architecture, user workflows, projects, files, and asynchronous processing**

Key contributions:

- Established the initial Django project structure
- Implemented the main project CRUD workflows
- Developed project ownership and permission logic
- Implemented public and private projects
- Added project membership and invitation workflows
- Added secure invitation tokens
- Implemented project likes and comments
- Added project sharing functionality
- Implemented multi-file and folder-based uploads
- Added project file browsing and downloads
- Improved project detail and edit workflows
- Migrated the project database to PostgreSQL
- Configured the pgvector-enabled PostgreSQL image
- Configured Celery with Redis
- Added asynchronous email tasks
- Added asynchronous project invitation emails
- Added email verification tasks
- Added user account, profile, and following functionality
- Supported global architecture, integration, and permission handling

### Person B — Zahra

GitHub: [@zahrazn21](https://github.com/zahrazn21)

**Primary responsibilities: Dashboard, notifications, search, discovery, and responsive interface**

Key contributions:

- Developed and refined the dashboard
- Created the sidebar and navigation interface
- Implemented project cards and explore views
- Developed the notification system
- Added notification context processing
- Implemented read and unread notification workflows
- Built the initial search application
- Added project and user search
- Added filters, result counts, and pagination
- Added recent search history and suggestions
- Migrated project search to Elasticsearch
- Added Elasticsearch document indexing
- Improved the project explore experience
- Integrated authentication and GitHub signup UI
- Added responsive interface improvements
- Added dark mode support
- Improved dashboard responsiveness
- Polished shared layouts, cards, and navigation

### Person C — Elyana Nasiri

GitHub: [@xElyanax](https://github.com/xElyanax)

**Primary responsibilities: UI/UX design, frontend implementation, activity tracking, feedback management, AI recommendations, and backend integration**

Key contributions:

- Designed the overall visual language and user interface of SkillSphere
- Implemented and refined the responsive frontend across the platform
- Created and improved shared layouts, navigation, cards, forms, and page structures
- Designed responsive behavior for desktop, tablet, and mobile screens
- Added dark mode compatibility and consistent component styling
- Implemented dashboard UI and integrated dynamic backend data into the interface
- Designed the AI recommendation section and project recommendation cards
- Added toast notification styling and shared static asset integration
- Improved the user experience of feedback, profile, authentication, and project-related pages
- Designed and implemented the `ActivityLog` model
- Added authentication activity signals
- Implemented activity logging middleware
- Created a centralized activity logging service
- Added request classification and metadata tracking
- Created the user activity history interface
- Designed and implemented the feedback system
- Added feedback forms, validation, statuses, ratings, and statistics
- Integrated feedback submissions with activity tracking
- Implemented the AI project recommendation engine using TF-IDF and cosine similarity
- Added recommendation scores, explanations, eligibility rules, and fallback behavior
- Integrated AI recommendations into the dashboard
- Supported dependency integration, testing, debugging, and merge conflict resolution
---

## Getting Started

### Prerequisites

Install the following tools:

- Python 3.12 or later
- Git
- Docker Desktop
- Node.js and npm
- Redis or Docker
- A virtual environment tool such as `venv`

---

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/Soyokaze00/SkillSphere.git
cd SkillSphere
```

### 2. Create and activate a virtual environment

#### macOS and Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Create an environment file

Create a `.env` file in the project root:

```env
DB_NAME=skillsphere
DB_USER=skillsphere
DB_PASSWORD=skillsphere
DB_HOST=localhost
DB_PORT=5433

EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-app-password
```

Do not commit the `.env` file.

### 5. Start PostgreSQL and Elasticsearch

```bash
docker compose up -d db elasticsearch
```

Check their status:

```bash
docker compose ps
```

PostgreSQL will be available on:

```text
localhost:5433
```

Elasticsearch will be available on:

```text
http://localhost:9200
```

### 6. Start Redis

Redis is used by Celery as its message broker.

Using Docker:

```bash
docker run \
  --name skillsphere_redis \
  -p 6379:6379 \
  -d redis:7-alpine
```

Verify Redis:

```bash
docker exec skillsphere_redis redis-cli ping
```

Expected output:

```text
PONG
```

### 7. Run database migrations

```bash
python manage.py migrate
```

### 8. Create an administrator

```bash
python manage.py createsuperuser
```

### 9. Build the Elasticsearch index

Make sure Elasticsearch is running, then execute:

```bash
python manage.py search_index --rebuild
```

### 10. Install Tailwind dependencies

```bash
python manage.py tailwind install
```

---

## Running the Application

The development environment uses multiple processes.

### Terminal 1 — PostgreSQL and Elasticsearch

```bash
docker compose up -d db elasticsearch
```

### Terminal 2 — Redis

```bash
docker start skillsphere_redis
```

### Terminal 3 — Celery Worker

```bash
source .venv/bin/activate
python -m celery -A skill_sphere worker --loglevel=info
```

For macOS development, the solo worker pool can be used:

```bash
python -m celery \
  -A skill_sphere worker \
  --loglevel=info \
  --pool=solo \
  --concurrency=1
```

### Terminal 4 — Tailwind CSS

```bash
source .venv/bin/activate
python manage.py tailwind start
```

### Terminal 5 — Django Development Server

```bash
source .venv/bin/activate
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

---

## GitHub Social Authentication

SkillSphere supports GitHub login through `django-allauth`.

To enable it locally:

1. Create a GitHub OAuth application.
2. Open the Django Admin panel.
3. Add a Social Application for the GitHub provider.
4. Add the current Django Site to the Social Application.
5. Enter the GitHub OAuth client ID and client secret.

The application remains usable through regular username and email authentication when GitHub OAuth is not configured.

---

## Useful Development Commands

### Django system check

```bash
python manage.py check
```

### Run tests

```bash
python manage.py test
```

### Create migrations

```bash
python manage.py makemigrations
```

### Apply migrations

```bash
python manage.py migrate
```

### Open the Django shell

```bash
python manage.py shell
```

### Rebuild the Elasticsearch index

```bash
python manage.py search_index --rebuild
```

### Check Docker services

```bash
docker compose ps
```

### Test Redis

```bash
docker exec skillsphere_redis redis-cli ping
```

### Start Celery

```bash
python -m celery -A skill_sphere worker --loglevel=info
```

### Build Tailwind once

```bash
python manage.py tailwind build
```

---

## Recommendation Engine Flow

```text
User Profile
    │
    ├── Username
    └── Biography
         │
         ▼
Text Normalization
         │
         ▼
TF-IDF Vectorization
         │
         ├─────────────────────────────┐
         │                             │
         ▼                             ▼
User Vector                 Project Content Vectors
                            ├── Title
                            ├── Description
                            └── Tags
         │                             │
         └──────────┬──────────────────┘
                    ▼
             Cosine Similarity
                    │
                    ▼
          Ranked Project Suggestions
                    │
                    ▼
       Match Score + Recommendation Reason
```

---

## Activity Tracking Flow

```text
Authenticated User Request
            │
            ▼
ActivityLogMiddleware
            │
            ├── Ignore static, media, admin, and auth paths
            ├── Accept state-changing HTTP methods
            └── Require a successful response
            │
            ▼
Request Classification Service
            │
            ▼
ActivityLog Record
            ├── User
            ├── Action
            ├── Description
            ├── Path
            ├── Method
            ├── Status
            ├── IP address
            └── Timestamp
```

---

## Feedback Flow

```text
Feedback Form
     │
     ▼
Form Validation
     │
     ▼
Feedback Service
     │
     ├── Save feedback
     ├── Attach authenticated user
     └── Create activity log
     │
     ▼
Feedback History and Admin Review
```

---

## Security and Production Notes

The current configuration is intended for local development and educational use.

Before production deployment:

- Move `SECRET_KEY` into environment variables
- Disable `DEBUG`
- Configure `ALLOWED_HOSTS`
- Use secure production email credentials
- Configure HTTPS
- Configure secure session and CSRF cookies
- Use a production WSGI or ASGI server
- Serve static and media files through a dedicated service
- Restrict PostgreSQL, Redis, and Elasticsearch network access
- Review OAuth callback URLs
- Configure Celery worker supervision
- Add automated backups
- Expand automated test coverage

---

## Future Improvements

Potential future enhancements include:

- Real-time project chat
- WebSocket notifications
- Rich project task boards
- Skill-specific user profiles
- Recommendation feedback and learning
- Hybrid collaborative recommendations
- Advanced project analytics
- File version history
- Team roles and granular permissions
- REST API support
- Expanded automated tests
- Production deployment configuration
- CI/CD workflows

---

## Contribution Workflow

1. Create a feature branch:

```bash
git switch -c feature/your-feature-name
```

2. Make and test your changes.

3. Commit with a meaningful message:

```bash
git add .
git commit -m "Add your feature description"
```

4. Push the branch:

```bash
git push -u origin feature/your-feature-name
```

5. Open a pull request into `main`.

Please keep unrelated changes in separate commits and run the following before opening a pull request:

```bash
python manage.py check
python manage.py test
```

---

## Authors

- **Nasim — Person A**  
  GitHub: [@Soyokaze00](https://github.com/Soyokaze00)

- **Zahra — Person B**  
  GitHub: [@zahrazn21](https://github.com/zahrazn21)

- **Elyana Nasiri — Person C**  
  GitHub: [@xElyanax](https://github.com/xElyanax)

---

<p align="center">
  Built collaboratively with Django, PostgreSQL, Elasticsearch, Celery, Redis, Tailwind CSS, and scikit-learn.
</p>
