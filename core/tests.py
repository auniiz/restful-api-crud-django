from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Employee, Position, Department, Status
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
from PIL import Image
import shutil
import os
from django.conf import settings


def create_temp_image():
    image = Image.new('RGB', (100, 100))
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(temp_file, 'jpeg')
    temp_file.seek(0)
    return temp_file


class SetupMixin(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='demo', password='demo123')
        self.client.login(username='demo', password='demo123')

        self.status = Status.objects.create(name='Active')
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

class EmployeeTests(SetupMixin):
    def test_list_employees(self):
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_employee(self):
        data = {
            'name': 'Jane Smith',
            'address': '456 Road',
            'manager': True,
            'status': self.status.id,
            'position': self.position.id,
            'department': self.department.id,
            'image': SimpleUploadedFile('new.jpg', create_temp_image().read(), content_type='image/jpeg')
        }
        response = self.client.post('/api/employees/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_employee(self):
        response = self.client.get(f'/api/employees/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.employee.name)

    def test_update_employee(self):
        data = {
            'name': 'John Updated',
            'address': 'New Address',
            'manager': True,
            'status': self.status.id,
            'position': self.position.id,
            'department': self.department.id
        }
        response = self.client.put(f'/api/employees/{self.employee.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Updated')

    def test_delete_employee(self):
        response = self.client.delete(f'/api/employees/{self.employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_employees_by_position(self):
        response = self.client.get(f'/api/employees/?position={self.position.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_employees_by_department(self):
        response = self.client.get(f'/api/employees/?department={self.department.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_employees_by_status(self):
        response = self.client.get(f'/api/employees/?status={self.status.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PositionTests(SetupMixin):
    def test_list_positions(self):
        response = self.client.get('/api/positions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_position(self):
        response = self.client.post('/api/positions/', {
            'name': 'Manager',
            'salary': 100000
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class DepartmentTests(SetupMixin):
    def test_list_departments(self):
        response = self.client.get('/api/departments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_department(self):
        response = self.client.post('/api/departments/', {
            'name': 'HR',
            'manager': self.employee.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class StatusTests(SetupMixin):
    def test_list_statuses(self):
        response = self.client.get('/api/statuses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_status(self):
        response = self.client.post('/api/statuses/', {
            'name': 'Probation'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='demo', password='demo123')

    def test_unauthenticated_access_denied(self):
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_access_allowed(self):
        self.client.login(username='demo', password='demo123')
        response = self.client.get('/api/employees/')
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)
