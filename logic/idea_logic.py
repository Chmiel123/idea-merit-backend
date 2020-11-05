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

def get_by_parent_id(parent_id: uuid) -> List[Idea]:
    return Idea.find_by_parent_id(parent_id)

def get_by_author_id(author_id: uuid) -> List[Idea]:
    return Idea.find_by_author_id(author_id)

def create_root_idea(name: str, content: str) -> Idea:
    new_idea = Idea(None, None, name, content, 0.0)
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
    author.subtract_resource(initial_resource)
    new_idea = Idea(parent_id, author.id, name, content, initial_resource)
    new_idea.save_to_db()
    vote_event = VoteEvent(VoteEventType.positive, author.id, new_idea.id, initial_resource)
    vote_event.save_to_db()
    return new_idea

def vote(votee: Account, idea_id: uuid, resource: float) -> str:
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
    found_idea.add_resource(resource)
    vote_event = VoteEvent(VoteEventType.positive, votee.id, found_idea.id, resource)
    vote_event.save_to_db()
    return 'Vote succesful'
