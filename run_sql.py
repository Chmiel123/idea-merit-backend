import sys
import os
import argparse

abspath = os.path.abspath(__file__)
path = os.path.dirname(abspath) + '\\src'
os.chdir(path)
sys.path.insert(1, path)

from config.config import Config
from model.db import DB, db

parser = argparse.ArgumentParser(description='Process some integers.', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('command', nargs='?',
                    help=
'''    create - Creates database, destroys first if exists.
    reset - Recreates database and inserts base data.
    insert_data - Inserts base data into the database.''')
parser.add_argument('--config', metavar='-c', type=str, dest='config',
                    default='',
                    help='Name of the config file (*name*_config.yml)')

args = parser.parse_args()
db = DB(Config(args.config))

from model.sql_create_db import sql_create_db
from model.sql_insert_data import sql_insert_data

if args.command == 'create':
    sql_create_db(db)
elif args.command == 'reset':
    sql_create_db(db)
    sql_insert_data(db)
elif args.command == 'insert_data':
    sql_insert_data(db)
else:
    parser.print_help()