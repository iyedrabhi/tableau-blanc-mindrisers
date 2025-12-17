# Restaurant Reservation System – Full Setup Guide

This guide covers setup for the complete Celery + Django Channels real-time notification system.

## Architecture Overview

- **Backend**: Django 5.2 with custom auth (CustomUser)
- **Task Queue**: Celery with Redis broker
- **Scheduler**: Celery Beat (periodic reminders)
- **Real-time**: Django Channels (WebSocket) + Redis channel layer
- **Database**: SQLite (development), adaptable to PostgreSQL

## Prerequisites

- Python 3.8+
- Redis (locally or Docker)
- pip

## Installation

### 1. Create and activate virtual environment

```bash
python -m venv env_restaurant
source env_restaurant/bin/activate  # Linux/Mac
# or
env_restaurant\Scripts\activate  # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install django==5.2.8 celery redis channels channels-redis asgiref
```

### 3. Start Redis

**Option A: Docker**

```bash
docker run -p 6379:6379 --name redis -d redis:7
```

**Option B: Local installation**

```bash
# Linux (Debian/Ubuntu)
sudo apt-get install redis-server
redis-server

# macOS
brew install redis
redis-server

# Windows: download from https://github.com/microsoftarchive/redis/releases
```

### 4. Apply migrations

```bash
cd restaurant_project
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser (staff account) to receive manager notifications

```bash
python manage.py createsuperuser
```

## Running the System

You need to run **4 services simultaneously** (in separate terminals):

### Terminal 1: Django Development Server

```bash
cd restaurant_project
python manage.py runserver 0.0.0.0:8000
```

Access the app at: `http://localhost:8000`

### Terminal 2: Celery Worker

```bash
cd restaurant_project
celery -A restaurant_project worker --loglevel=info
```

The worker processes tasks: reminders, timers, prolongations, releases, notifications.

### Terminal 3: Celery Beat Scheduler

```bash
cd restaurant_project
celery -A restaurant_project beat --loglevel=info
```

Beat scheduler runs periodic tasks (e.g., dispatch reminders every minute).

### Terminal 4 (Optional): Daphne ASGI for production-like WebSocket handling

```bash
cd restaurant_project
pip install daphne
daphne -b 0.0.0.0 -p 8000 restaurant_project.asgi:application
```

(Note: `runserver` in Terminal 1 already handles WebSockets for development; use Daphne for production.)

## Run Tests

```bash
cd restaurant_project
python manage.py test reservations
```

Tests cover:

- Task creation and task ID storage
- Signal-triggered timer scheduling
- Release task revocation on cancellation
- Channel layer notification sending
- Error handling for missing channel layer

## Usage Flow

### Client Flow

1. **Login** as a client user
2. Navigate to **"Make a Reservation"**
3. Select date, time, number of people
4. View **filtered available tables** (by category, location, accessibility, etc.)
5. Click **"Reserve"** to book a table
   - Duration is automatically computed from start/end time
   - A reminder is scheduled (2h or 4h before, depending on reservation time)
   - Release task is scheduled for end of duration + 3-minute grace period
6. View your **"My Reservations"** to see upcoming reservations
7. Click **"Extend"** to request more time (prolongation)
   - Previous release task is revoked and a new one is scheduled
   - Manager is notified of the prolongation
8. Receive **real-time notifications** as a toast in the top-right corner:
   - Reservation reminders
   - Prolongation confirmations
   - Table release confirmations

### Manager Flow

1. **Login** as staff user
2. View **"Manager Dashboard"** to see all tables and reservations
3. Receive **real-time notifications** (WebSocket) whenever:
   - A client makes a new reservation
   - A client cancels a reservation
   - A client requests prolongation
   - A table is automatically released
4. View **"All Notifications"** to see notification history

## Configuration

### Environment Variables (Optional)

Create a `.env` file or set these in your system:

```bash
# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Channels
CHANNEL_REDIS_URL=redis://localhost:6379

# Email (for email notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@restaurant.com
```

Then update `settings.py` to load from environment:

```python
import os
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
# etc.
```

### Debugging

- **Worker logs**: Watch Terminal 2 for task execution and errors
- **Beat logs**: Watch Terminal 3 for scheduled task dispatch
- **WebSocket logs**: Check browser DevTools Console (F12) for WebSocket messages
- **Django logs**: Watch Terminal 1 for HTTP requests and errors

## Common Issues

### "Connection refused" Redis error

- Ensure Redis is running: `redis-cli ping` should return `PONG`
- Check Redis port (default 6379): `redis-cli info server`

### WebSocket connection fails ("Connection refused")

- Ensure worker and beat are running
- Check that `daphne` is running on the correct port (if using Daphne instead of `runserver`)
- In browser Console, check if WebSocket URL is correct: `ws://localhost:8000/ws/notifications/`

### Notifications not appearing

- Check that user is authenticated (login required)
- Check browser Console for WebSocket errors
- Verify that notification channel layer is not raising exceptions (see worker logs)

### Tasks not executing

- Ensure Celery worker is running and connected to broker
- Check worker logs for task exceptions
- Verify task is being sent (check django logs or worker output)

## Next Steps

### Advanced Features (Future)

- Add SMS notifications via Twilio (requires API keys)
- Add email digest summaries
- Implement reservation history and analytics dashboard
- Add table capacity optimization AI
- Multi-restaurant support
- Mobile app integration

### Production Deployment

- Use PostgreSQL instead of SQLite
- Configure gunicorn/uWSGI for WSGI + Daphne for ASGI
- Set up supervisor/systemd for process management
- Use Redis Sentinel for high availability
- Enable SSL/TLS for WebSockets (wss://)
- Add monitoring (Celery Flower, Prometheus, etc.)

## Project Structure

```
restaurant_project/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── restaurant_project/
│   ├── __init__.py
│   ├── asgi.py          # Channels ProtocolTypeRouter
│   ├── celery.py        # Celery app config
│   ├── routing.py       # WebSocket routing
│   ├── settings.py      # All Django + Celery + Channels config
│   ├── urls.py
│   ├── wsgi.py
│   └── views.py
├── reservations/
│   ├── models.py        # Reservation, Notification models
│   ├── views.py         # Client/manager views
│   ├── tasks.py         # Celery tasks (timers, reminders, releases, prolongations)
│   ├── signals.py       # Django signals (reminder calc, timer scheduling, revocation)
│   ├── consumers.py     # Channels WebSocket consumer
│   ├── urls.py
│   ├── services/
│   │   └── notifications.py  # DB + channel layer notification functions
│   ├── management/
│   │   └── commands/
│   │       └── send_reminders.py
│   ├── templates/
│   │   └── reservations/
│   │       ├── create_reservation.html
│   │       ├── my_reservations.html
│   │       ├── extend_confirm.html
│   │       ├── notifications.html
│   │       └── preferences.html
│   └── tests/
│       └── test_tasks_signals.py
├── tables/
│   ├── models.py        # Table model with advanced filtering fields
│   ├── views.py
│   └── urls.py
├── client/
│   ├── models.py        # CustomUser, NotificationPreference
│   └── ...
├── static/
│   ├── css/
│   │   └── notifications.css  # Toast notification styles
│   └── js/
│       └── notifications.js   # WebSocket client
└── templates/
    └── base.html        # Base template with static resources
```

## Support

For issues or questions, review:

- Django Channels docs: https://channels.readthedocs.io/
- Celery docs: https://docs.celeryproject.org/
- Django docs: https://docs.djangoproject.com/
