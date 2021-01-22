import django
django.setup()

class MyTestCase(django.test.TestCase):
    def test_something(self):
        self.assertEqual(True, False)
