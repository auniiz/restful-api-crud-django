from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Employee, Position, Department, Status
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from PIL import Image

# Create your tests here.
class StatusModelTest(TestCase):
    def test_create_status(self):
        status = Status.objects.create(name="In Probation")
        self.assertEqual(str(status), "In Probation")

def create_temp_image():
    image = Image.new('RGB', (100, 100))
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(temp_file, 'jpeg')
    temp_file.seek(0)
    return temp_file

class EmployeeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='demo', password='demo123')
        self.client.login(username='demo', password='demo123')

        self.status = Status.objects.create(name='active')
        self.position = Position.objects.create(name='Developer', salary=80000)
        self.department = Department.objects.create(name='Engineering', manager=None)

        self.image = SimpleUploadedFile('test.jpg', create_temp_image().read(), content_type='image/jpeg')

        self.employee = Employee.objects.create(
            name='John Doe',
            address='123 Street',
            manager=False,
            status=self.status,
            position=self.position,
            department=self.department,
            image=self.image,
        )

    def test_create_employee(self):
        url = '/api/employees/'
        data = {
            'name': 'Jane Smith',
            'address': '456 Road',
            'manager': True,
            'status': self.status.id,
            'position': self.position.id,
            'department': self.department.id,
            'image': SimpleUploadedFile('test2.jpg', create_temp_image().read(), content_type='image/jpeg')
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_employees(self):
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_employee(self):
        response = self.client.get(f'/api/employees/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe')

    def test_update_employee(self):
        url = f'/api/employees/{self.employee.id}/'
        data = {
            'name': 'John Updated',
            'address': 'New Address',
            'manager': False,
            'status': self.status.id,
            'position': self.position.id,
            'department': self.department.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Updated')

    def test_delete_employee(self):
        response = self.client.delete(f'/api/employees/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
