from app import app

"""
WSGI (Web Server Gateway Interface) entry point for the application.
This file is used by production WSGI servers like Gunicorn to run the application.
"""

if __name__ == "__main__":
    app.run()
