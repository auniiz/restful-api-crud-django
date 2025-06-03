from django.test import TestCase

# Create your tests here.
class StatusModelTest(TestCase):
    def test_create_status(self):
        status = Status.objects.create(name="In Probation")
        self.assertEqual(str(status), "In Probation")
