import urllib.request
from google.auth import default
from google.auth.transport.requests import Request
import google.auth
credentials, project = google.auth.default()
# Wait, I don't have google.auth in python
