import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://ciphacpa:EBzLUPsS-_F01lnMWlTWbZ9j-GvwxOBW@ruby.db.elephantsql.com:5432/ciphacpa'
