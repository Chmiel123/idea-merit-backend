import sys

from config.config import Config
from model.db import DB
from model.sql_create_db import sql_create_db

config = ''
if len(sys.argv) > 1:
    config = sys.argv[1]

db = DB(Config(config))
sql_create_db(db)

# print 'Number of arguments:', len(sys.argv), 'arguments.'
# print 'Argument List:', str(sys.argv)