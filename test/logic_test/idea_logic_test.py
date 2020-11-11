import unittest
import uuid
from test.db_base_test_case import DBBaseTestCase
from config.config import config
from util.exception import IMException
from model.profile.account import Account
from logic import idea_logic

class IdeaLogicTest(DBBaseTestCase):
    def test_vote_deep_idea_tree(self):
        a = Account('user')
        a.virtual_resource_accrued = 2000
        a.save_to_db()
        self.assertGreaterEqual(a.get_total_resource(), 2000)

        root = idea_logic.create_root_idea('root', 'root content')
        self.assertTrue(root.is_root())

        idea1 = idea_logic.create_idea(a, root.id, 'idea1', 'content', 0)
        self.assertFalse(idea1.is_root())
        idea2 = idea_logic.create_idea(a, idea1.id, 'idea2', 'content', 0)
        idea3 = idea_logic.create_idea(a, idea2.id, 'idea3', 'content', 0)
        idea4 = idea_logic.create_idea(a, idea3.id, 'idea4', 'content', 0)
        idea5 = idea_logic.create_idea(a, idea4.id, 'idea5', 'content', 0)
        idea6 = idea_logic.create_idea(a, idea5.id, 'idea6', 'content', 0)

        idea_logic.vote(a, idea6.id, 1024)
        self.assertAlmostEqual(1024 * config['vote']['vote_resource_multiplier'], idea6.remaining_life(), 3)
        self.assertAlmostEqual(512 * config['vote']['vote_resource_multiplier'], idea5.remaining_life(), 3)
        self.assertAlmostEqual(256 * config['vote']['vote_resource_multiplier'], idea4.remaining_life(), 3)
        self.assertAlmostEqual(128 * config['vote']['vote_resource_multiplier'], idea3.remaining_life(), 3)
        self.assertAlmostEqual(64 * config['vote']['vote_resource_multiplier'], idea2.remaining_life(), 3)
        self.assertAlmostEqual(32 * config['vote']['vote_resource_multiplier'], idea1.remaining_life(), 3)
        self.assertAlmostEqual(0, root.remaining_life(), 3)

    def test_find(self):
        a = Account('user')
        a.virtual_resource_accrued = 2000
        a.save_to_db()
        self.assertGreaterEqual(a.get_total_resource(), 2000)

        root = idea_logic.create_root_idea('root', 'root content')
        self.assertTrue(root.is_root())

        idea1 = idea_logic.create_idea(a, root.id, 'idea1', 'content', 0)
        idea2 = idea_logic.create_idea(a, root.id, 'idea2', 'content', 0)
        self.assertFalse(idea1.is_root())

        idea = idea_logic.get_by_id(root.id)
        self.assertEqual(idea, root)
        idea = idea_logic.get_by_name('root')
        self.assertEqual(idea, root)
        idea = idea_logic.get_by_author_id(a.id)
        self.assertEqual(idea[0], idea1)
        self.assertEqual(idea[1], idea2)
        idea = idea_logic.get_by_parent_id(root.id)
        self.assertEqual(idea[0], idea1)
        self.assertEqual(idea[1], idea2)

    def test_create_idea(self):
        a = Account('user')
        a.virtual_resource_accrued = 2000
        a.save_to_db()
        self.assertGreaterEqual(a.get_total_resource(), 2000)

        root = idea_logic.create_root_idea('root', 'root content')
        self.assertTrue(root.is_root())

        idea1 = idea_logic.create_idea(a, root.id, 'idea1', 'content', 0)

        self.assertRaises(IMException, idea_logic.create_idea, a, root.id, 'idea2', 'content', 3000)
        self.assertRaises(IMException, idea_logic.create_idea, a, root.id, 'idea2', 'content', -1)
        self.assertRaises(IMException, idea_logic.create_idea, a, None, 'idea2', 'content', 3000)
        self.assertRaises(IMException, idea_logic.create_idea, a, root.id, 'idea1', 'content', 1000)
        self.assertRaises(IMException, idea_logic.create_idea, a, uuid.uuid4(), 'idea1', 'content', 1000)

    def test_vote(self):
        a = Account('user')
        a.virtual_resource_accrued = 2000
        a.save_to_db()
        self.assertGreaterEqual(a.get_total_resource(), 2000)

        root = idea_logic.create_root_idea('root', 'root content')
        self.assertTrue(root.is_root())

        idea1 = idea_logic.create_idea(a, root.id, 'idea1', 'content', 0)

        self.assertRaises(IMException, idea_logic.vote, a, idea1.id, 3000)
        self.assertRaises(IMException, idea_logic.vote, a, idea1.id, -1)
        self.assertRaises(IMException, idea_logic.vote, a, uuid.uuid4(), 1)
        self.assertRaises(IMException, idea_logic.vote, a, None, 1)
        self.assertRaises(IMException, idea_logic.vote, None, idea1.id, 1)

        idea_logic.vote(a, idea1.id, 2000)



if __name__ == '__main__':
    unittest.main()