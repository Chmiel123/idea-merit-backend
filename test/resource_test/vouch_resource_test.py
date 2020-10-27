import unittest
import json

from test.app_base_test_case import AppBaseTestCase
from model.profile.account import Account
from model.profile.email_verification import EmailVerification

class VouchResourceTest(AppBaseTestCase):
    def test_make_vouch_request(self):
        #TODO: keep track of multiple logins
        u1 = self.register_and_login()
        u2 = self.register_and_login('user2')

        result = self.post_auth(
            '/vouch/vouch_request',
            dict(
                top_id = u1['id'],
                bottom_id = u2['id']
            )
        )
        self.assertEqual(result.json['status'], 'Ok')
        result = self.get_auth(
            '/vouch/vouch_request'
        )
        self.assertEqual(len(result.json), 1)
        self.assertEqual(result.json[0]['top_accept'], False)
        self.assertEqual(result.json[0]['bottom_accept'], True)