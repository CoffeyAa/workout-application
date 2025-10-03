# Workout Tracker Django App

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Django](https://img.shields.io/badge/Django-4.3-green) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)

A **Django web application** to track workouts, exercises, personal records, and accomplishments (badges). Users can log workouts, track sets, monitor progress, and earn badges for hitting goals or streaks.

---

## Features

- Track workouts with multiple exercises.
- Log **sets** for each exercise with **reps, weight, duration, and unit (kg/lb)**.
- Track **personal records** for exercises (weighted or timed).
- Categorize exercises by **body part** and **exercise type**.
- Add **exercise images** for guidance.
- Earn **accomplishments / badges** based on streaks, PRs, or milestones.
- View progress metrics and exercise history.

---

## Tech Stack

- **Backend:** Django 4.x
- **Database:** PostgreSQL
- **Python version:** 3.11+
- **Optional tools:** `Black` for code formatting, `pre-commit` hooks

---

## Database Models Overview

- **User** – built-in Django User model.
- **Exercise** – contains name, categories, body parts, and images.
- **Workout** – logs workouts by a user.
- **WorkoutExercise** – exercises within a workout.
- **WorkoutSet** – reps, weight, duration, unit, order for each set.
- **PersonalRecord** – tracks best performance for exercises.
- **Accomplishment** – badges that users can earn.
- **UserAccomplishment** – badges earned by a user.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/workout-tracker.git
cd workout-tracker
```

### 2. Create a virtual environment

```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root (same level as `manage.py`):

```
POSTGRES_DB=workout_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
SECRET_KEY=your_django_secret_key
DEBUG=True
```

**Note:** Add `.env` to your `.gitignore` so it is not committed.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

### 8. Visit the app
Open your browser and go to http://localhost:8000 to see the app running.
