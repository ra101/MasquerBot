run:
	gunicorn wsgi:application --preload
