"""
The reason we're importing Django here and doing setup is to allow debugging with Pycharm interactive debugger
not with the Django Command, significant important in testing experience.
"""

import django

django.setup()
from django.test import TestCase


class Test(TestCase):
    raise NotImplementedError
