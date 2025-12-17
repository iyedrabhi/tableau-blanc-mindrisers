Celery setup (Option A) — quick start

Prerequisites

- Redis running locally (recommended) or another supported broker.
- Python deps: `celery`, `redis` drivers (e.g. `redis`), and your project's requirements installed.

Install (venv activated):

```bash
pip install celery redis
```

Start Redis (example on Windows with WSL or Linux):

```bash
# on Debian/Ubuntu
sudo apt update && sudo apt install redis-server -y
sudo service redis-server start
# or via docker
docker run -p 6379:6379 --name redis -d redis:7
```

Run Celery worker and beat

```bash
# from project root (where manage.py lives)
# start a worker
celery -A restaurant_project worker --loglevel=info

# in another terminal, start beat scheduler (or run both via systemd / supervisor)
celery -A restaurant_project beat --loglevel=info
```

Environment variables

- `CELERY_BROKER_URL`: broker URI (default redis://localhost:6379/0)
- `CELERY_RESULT_BACKEND`: result backend (defaults to broker)
- Configure email settings in `settings.py` or via environment variables (`EMAIL_HOST`, `EMAIL_PORT`, etc.)

Notes

- The project includes a periodic beat schedule that calls `reservations.tasks.dispatch_due_reminders` every minute.
- The signal on reservation creation schedules the reservation timer (release) via Celery.
- For production use, consider running workers with process managers and securing Redis.
