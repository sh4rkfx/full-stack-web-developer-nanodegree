"""Default config settings."""

DEBUG = True
SECRET_KEY = ''
# SQLALCHEMY_DATABASE_URI = "postgresql://caleb:abc.123@localhost/caleb_db"
SQLALCHEMY_DATABASE_URI = "sqlite:///caleb_test.db"
SQLALCHEMY_TRACK_MODIFICATIONS = True
WTF_CSRF_ENABLED = True
GOOGLE_ID = "455784998098-jm1oa2jn0mflhq2b5k7qt17imosmqppb.apps.googleusercontent.com"
GOOGLE_SECRET = "qhmJ01jyozz9twWLYoj8xmK7"
