"""
This is needed in order to use the Pycharm debugger when running tests.
Also, when running test files, use the configurations of this file in every test
"""
import django

django.setup()
from django.test import TestCase

from data.Resources import GetAuthTokenFactory


class BaseScrTestCase(TestCase):
    def get_token(self, resource):
        return GetAuthTokenFactory.get_auth_token(resource=resource)
