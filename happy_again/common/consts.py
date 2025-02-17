ADMIN_PASS = '0123456789'
USER_CONFIRMATION_TOKEN_EXPIRY_DELTA = 2

# Use this URL only for development
deployment = False


if deployment:
    # Use the following URL for deployment on the university server, to be updated
    SITE_URL = 'https://happyagain.essex.ac.uk:443'
    BASE_PATH = '/var/www/happy-again-backend/happy_again'
else:
    SITE_URL = 'http://localhost:1234'
    AUTH_LINK = "http://127.0.0.1:1234/users/verify"
    BASE_PATH = './happy_again'

SUBJECT_USER_CONFIRMATION_EMAIL = 'User Confirmation Email'
# SUBJECT_USER_RESET_PASSWORD = 'User reset password'
HAPPY_AGAIN_NO_REPLY_EMAIL = 'happyagainessex@gmail.com'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
