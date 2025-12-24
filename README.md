# ExamAssist (Morocco) - Backend API

**ExamAssist** is a RESTful API designed to bridge the gap between University students (Requesters) with disabilities and High School volunteers (Scribes) in Morocco. The system handles exam requests based on the Moroccan LMD (Licence-Master-Doctorat) academic system.

##  Project Status: Phase 3 (Core Architecture)
Currently, the project has the **Database Architecture** and **Django Skeleton** fully implemented.

### Current Features
*   **User Roles:** Distinction between **Requesters** (University Students) and **Scribes** (Volunteers).
*   **Moroccan Context:** Profiles store academic levels (e.g., "2ème Bac", "Licence").
*   **Exam Requests:** Tracks University, Faculty, Branch, and specific Modules.
*   **Application System:** A logical matching system ensuring unique applications per exam.

##  Technology Stack
*   **Python 3.10+**
*   **Django 6.0**
*   **Django REST Framework**
*   **Database:** SQLite (Development) / PostgreSQL (Production - Planned)

##  Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/AISalah/exam-assist-api.git
    cd exam-assist-api
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Database Migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Run Development Server**
    ```bash
    python manage.py runserver
    ```

##  Database Schema (Models)
*   **User:** Standard Authentication.
*   **Profile:** One-to-One link with User. Stores `role` (Requester/Scribe) and `academic_level`.
*   **ExamRequest:** Stores exam details (University, Faculty, Date, Status).
*   **Application:** Connects a `Scribe` to an `ExamRequest` with status tracking (Pending/Accepted). Includes constraints to prevent duplicate applications.

##  Roadmap
*   [x] **Part 1-3:** Project Setup & Database Design.
*   [ ] **Part 4:** Authentication (JWT) & API Endpoints.
*   [ ] **Part 5:** Deployment & Final Polish.

# ExamAssist (Morocco) - Backend API


**API Base URL:** 

`https://exam-assist-api.onrender.com/api/v1/`
