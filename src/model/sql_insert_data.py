from src.config.config import config, get
from src.model.system.idea import Idea

def sql_insert_data(db):
    raw = get('config/root_ideas.yml')
    for raw_idea in raw:
        found = Idea.find_by_name(raw_idea['name'])
        if (not found):
            i = Idea(None, None, raw_idea['name'], raw_idea['content'])
            i.save_to_db()
