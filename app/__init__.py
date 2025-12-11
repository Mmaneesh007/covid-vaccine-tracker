# COVID-19 Vaccine Tracker - App Module

# Expose the FastAPI application instance at the package level so
# process managers like gunicorn can import `app:app`.
try:
	from .api.main import app as app  # type: ignore
except Exception:
	# Import errors should not prevent module import; they will surface
	# when the server process attempts to start the application.
	app = None
