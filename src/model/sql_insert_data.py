from src.config.config import config, get
from src.model.system.idea import Idea

def sql_insert_data(db):
    raw = get('config/root_ideas.yml')
    inserted = dict()
    for raw_idea in raw:
        found = Idea.find_by_name(raw_idea['name'])
        if (not found):
            parent_id = None
            if ('parent' in raw_idea):
                parent_id = inserted[raw_idea['parent']]
            i = Idea(parent_id, None, raw_idea['name'], raw_idea['content'])
            i.save_to_db()
            inserted[i.name] = i.id

