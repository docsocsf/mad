# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p2kp70aidc@i0%z6a60yr%i8@s18mn44g+1kfv8-=d5!)sb_@4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DOMAIN_URL = 'http://127.0.0.1:8000'

# Priorities when matching students
POINTS_FOR_PARTY_MATCH = 2
POINTS_FOR_INTEREST_MATCH = 1
EXPECTED_CHILDREN = 180

# Registration settings
ALLOW_PARENT_REGISTRATION = True
ALLOW_CHILD_REGISTRATION = False

# Mailing settings
SEND_EMAILS = False
HOST = "smtp.office365.com"
PORT = 587
TLS = True
FROM = "example@ic.ac.uk"
USER = "example@ic.ac.uk"
PASSWORD = "password"

# Settings
ALLOWED_HOSTS = []
