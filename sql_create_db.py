import os
import os.path
import importlib

from config.config import Config
from model.db import DB

# db = DB(Config('test'))
db = DB(Config())
schemas = []

file_dir = os.path.realpath('model')
print(file_dir)
for (dirpath, dirnames, filenames) in filter(lambda x: not x[0].endswith('__pycache__') and x[0] != file_dir, os.walk(file_dir)):

    schema = os.path.basename(dirpath)
    if schema not in schemas:
        schemas.append(schema)
    for filename in filenames:
        filename_without_extension = os.path.splitext(filename)[0]
        fullname = f'model.{schema}.{filename_without_extension}'
        print(fullname)
        importlib.import_module(fullname)



for schema in schemas:
    db.engine.execute(f'DROP SCHEMA IF EXISTS {schema} CASCADE')
    db.engine.execute(f'CREATE SCHEMA IF NOT EXISTS {schema}')
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
db.Base.metadata.drop_all(db.engine)
db.Base.metadata.create_all(db.engine)