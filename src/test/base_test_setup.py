from config.config import Config
from model.db import DB

db = DB(Config('test'))
