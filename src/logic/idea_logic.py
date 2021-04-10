import uuid
from typing import List
from config.config import config
from util.exception import IMException
from model.profile.account import Account
from model.system.idea import Idea
from model.event.vote_event import VoteEvent, VoteEventType

def get_by_id(id: uuid) -> Idea:
    return Idea.find_by_id(id)

def get_by_name(name: str) -> Idea:
    return Idea.find_by_name(name)

def get_by_parent_id(parent_id: uuid, page: int = 0) -> List[Idea]:
    if page is not None:
        return Idea.find_by_parent_id(parent_id, page)
    return Idea.find_by_parent_id(parent_id)

def get_by_author_id(author_id: uuid, page: int = 0) -> List[Idea]:
    if page is not None:
        return Idea.find_by_author_id(author_id, page)
    return Idea.find_by_author_id(author_id)

def get_root_ideas(page: int = 0) -> List[Idea]:
    if page is not None:
        return Idea.find_by_parent_id(None, page)
    return Idea.find_by_parent_id(None)

def create_root_idea(name: str, content: str) -> Idea:
    new_idea = Idea(None, None, name, content)
    new_idea.save_to_db()
    return new_idea

def create_idea(author: Account, parent_id: uuid, name: str, content: str, initial_resource: float) -> Idea:
    if author.get_total_resource() < initial_resource:
        raise IMException('Not enough resource')
    if initial_resource < 0:
        raise IMException('Cannot vote with negative resource')
    if not parent_id:
        raise IMException('Parent idea not specified')
    found_parent = Idea.find_by_id(parent_id)
    if not found_parent:
        raise IMException('Parent idea not found')
    found_duplicate = Idea.find_by_name_and_parent(name, parent_id)
    if found_duplicate:
        raise IMException('Idea with the same name already exists')
    
    author.subtract_resource(initial_resource)
    new_idea = Idea(parent_id, author.id, name, content)
    add_resource_direct(new_idea, initial_resource * config['vote']['vote_resource_multiplier'])
    new_idea.save_to_db()
    vote_event = VoteEvent(VoteEventType.positive, author.id, new_idea.id, initial_resource)
    vote_event.save_to_db()
    return new_idea

def vote(votee: Account, idea_id: uuid, resource: float) -> str:
    if not votee:
        raise IMException('Invalid votee')
    if votee.get_total_resource() < resource:
        raise IMException('Not enough resource')
    if not idea_id:
        raise IMException('Invalid idea id')
    if resource < 0:
        raise IMException('Cannot vote with negative resource')
    found_idea = Idea.find_by_id(idea_id)
    if not found_idea:
        raise IMException('Idea not found')
    votee.subtract_resource(resource)
    add_resource_direct(found_idea, resource * config['vote']['vote_resource_multiplier'])
    vote_event = VoteEvent(VoteEventType.positive, votee.id, found_idea.id, resource)
    vote_event.save_to_db()
    return 'Vote succesful'

def add_resource_direct(idea: Idea, resource: float):
    idea.add_resource_direct(resource)
    parent_idea = Idea.find_by_id(idea.parent_id)
    if parent_idea and not parent_idea.is_root():
        add_resource_inherit(parent_idea, resource / 2.0)

def add_resource_inherit(idea: Idea, resource: float):
    idea.add_resource_inherited(resource)
    parent_idea = Idea.find_by_id(idea.parent_id)
    if parent_idea and not parent_idea.is_root():
        add_resource_inherit(parent_idea, resource / 2.0)