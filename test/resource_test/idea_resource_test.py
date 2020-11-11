import unittest
import json
import datetime
import uuid

from test.app_base_test_case import AppBaseTestCase
from config.config import config
from model.system.idea import Idea
from model.profile.account import Account
from model.profile.email_verification import EmailVerification
from logic import idea_logic

class IdeaResourceTest(AppBaseTestCase):

    def test_create_idea_and_get(self):
        self.register_and_login('user1')

        a1 = Account.find_by_username('user1')
        a1.virtual_resource_accrued = 1000
        a1.save_to_db()

        root_idea =idea_logic.create_root_idea('root', 'root content.')
        # root_idea = Idea.find_by_name('root')

        result = self.post_auth(
            '/idea',
            dict(
                parent_id = str(root_idea.id),
                name = 'idea1',
                content = 'Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1.',
                initial_resource = 48
            )
        )
        self.assertEqual(result.json['status'], 'Ok')

        result = self.get_auth(
            f'/idea?name=idea1'
        )
        self.assertEqual(result.json['name'], 'idea1')
        id = result.json['id']

        result = self.post_auth(
            '/idea',
            dict(
                parent_id = str(id),
                name = 'idea2',
                content = 'Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1.',
                initial_resource = 48
            )
        )
        self.assertEqual(result.json['status'], 'Ok')

        result = self.get_auth(
            f'/idea?id={id}'
        )
        self.assertEqual(result.json['name'], 'idea1')
        result = self.get_auth(
            f'/idea?parent_id={id}'
        )
        self.assertEqual(result.json[0]['name'], 'idea2')
        result = self.get_auth(
            f'/idea?author_id={a1.id}'
        )
        self.assertEqual(result.json[0]['name'], 'idea1')
        self.assertEqual(result.json[1]['name'], 'idea2')
        result = self.get_auth(
            f'/idea'
        )
        self.assertEqual(result.json['status'], 'Error')
        result = self.get_auth(
            f'/idea?name=idea3'
        )
        self.assertEqual(result.json['status'], 'Error')
        result = self.get_auth(
            f'/idea?id={uuid.uuid4()}'
        )
        self.assertEqual(result.json['status'], 'Error')

    def test_vote_idea(self):
        self.register_and_login('user1')

        a1 = Account.find_by_username('user1')
        a1.virtual_resource_accrued = 72
        a1.save_to_db()

        root_idea =idea_logic.create_root_idea('root', 'root content.')
        # root_idea = Idea.find_by_name('root')

        result = self.post_auth(
            '/idea',
            dict(
                parent_id = str(root_idea.id),
                name = 'idea1',
                content = 'Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1. Content1 is a content1.',
                initial_resource = 48
            )
        )
        self.assertEqual(result.json['status'], 'Ok')

        idea = Idea.find_by_name('idea1')

        result = self.post_auth(
            '/idea/vote',
            dict(
                idea_id = str(idea.id),
                resource = 24
            )
        )
        self.assertEqual(result.json['status'], 'Ok')
        idea = Idea.find_by_name('idea1')
        
        self.assertAlmostEqual(idea.remaining_life(), 72 * config['vote']['vote_resource_multiplier'], 3)
        