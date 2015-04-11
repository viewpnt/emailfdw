"""
Test emailfdw's various SELECT operators
"""

import unittest
import os
from urlparse import urlparse

from emailfdw.tests import create_db
from emailfdw.tests import drop_db
from emailfdw.tests import sqlalchemy_engine
from emailfdw.tests import sqlalchemy_session
from emailfdw.tests import MaxEmail

import mock

import logging
logging.basicConfig(level=logging.INFO)

class SelectTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = sqlalchemy_engine()
        create_db(self.engine)
        self.session = sqlalchemy_session(self.engine)

    def test_simple_select(self):
        result = self.session.query(MaxEmail).all()
        #import ipdb; ipdb.set_trace()
        self.assert_(result)

    '''
    def test_payload_select(self):#, search_mock, fetch_mock):
        result = self.session.query(MaxEmail).values("Message-ID", "payload")
        import ipdb; ipdb.set_trace()
        self.assert_(result)
    '''

    def tearDown(self):
        self.session.close()
        drop_db(self.engine)


if __name__ == '__main__':
    unittest.main()
