from django.test import TestCase
from rest_framework.test import APITestCase
import csv, io
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status
from users.models import User


class UploadFileViewTest(APITestCase):

    def setUp(self):
        # set up url to reach to the UploadCSVFileView for test methods
        self.url = '/upload/'
    
    def create_csv_file(self, data):
        """
        Util function to create a csv file for all test methods, with 
        the given data input depending on test method
        """
    
        csv_data = io.StringIO() # initialize in memory file like object with empty string
        writer = csv.writer(csv_data)
        writer.writerow(['name', 'email', 'age']) # write column headers

        for row in data:
            writer.writerow(row)
        
        csv_data.seek(0) # change position of file handler to the beginning
        
        return InMemoryUploadedFile(csv_data, 'file', 'test.csv', 'text/csv', csv_data.tell(), None)
    
    def test_valid_csv_file(self):
        """
        Create user instances and respond with 200 ok for a valid csv file
        """
        data = [
            ['John', 'john@gmail.com', 50],
            ['Ben', 'ben@gmail.com', 45]
        ]
        file = self.create_csv_file(data)
        data = {'file': file}

        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rejected_records_count'], 0)
        self.assertEqual(response.data['saved_records_count'], 2)
        self.assertEqual(User.objects.count(), 2)
      

    
    def test_upload_invalid_file(self):
        """
        Check the file type and return an error message and 400 bad request if not csv
        """
        
        text_file = InMemoryUploadedFile(
            io.StringIO('Dummy text'), 'file', 'test.txt', 'text/plain', 0, None
            )
        data = {'file': text_file}

        response = self.client.post(self.url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'File should be in CSV format')

    def test_incomplete_row_in_csv(self):
        """
        Reject the row if any of the fields name, email, age is missing and increase the rejected records count by 1
        """
        data = [
            ['John', 'abc@gmail.com'],
            ['Ben', 'abc@gmail.com', 45]
        ]
        file = self.create_csv_file(data)
        data = {'file': file}

        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rejected_records_count'], 1)
        self.assertEqual(response.data['saved_records_count'], 1)
        self.assertIn('errors', response.data)
        self.assertIn('Incomplete row', response.data['errors'][0])

    def test_non_empty_name(self):
        """
        Reject the record with empty name and increase the rejected records count by 1
        """
        data = [
            ['', 'abc@gmail.com', 30],
            ['Ben', 'abc@gmail.com', 45]
        ]
        file = self.create_csv_file(data)
        data = {'file': file}

        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('rejected_records_count', response.data)
        self.assertEqual(response.data['rejected_records_count'], 1)
        self.assertEqual(response.data['saved_records_count'], 1)
        self.assertIn('errors', response.data)
        self.assertIn('name', response.data['errors'][0])


    def test_duplicate_email(self):
        """
        Reject the user and increase the rejected_records_count by 1  if the email already exists in the user table in the database
        """
        data = [
            ['John', 'abc@gmail.com', 30],
            ['Ben', 'abc@gmail.com', 45]
        ]
        file = self.create_csv_file(data)
        data = {'file': file}

        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('rejected_records_count', response.data)
        self.assertEqual(response.data['rejected_records_count'], 1)
        self.assertIn('errors', response.data)
        self.assertIn('email', response.data['errors'][0])

    def test_age_limit(self):
        """
        Age should be between 0 and 120 else reject the user and increase the rejected records count by 1
        """
        data = [
            ['John', 'john@gmail.com', -2],
            ['David', 'david@gmail.com', 30],
            ['Aby', 'aby@gmail.com', 125]
        ]

        file = self.create_csv_file(data)
        data = {'file': file}

        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('rejected_records_count', response.data)
        self.assertEqual(response.data['rejected_records_count'], 2)
        self.assertEqual(response.data['saved_records_count'], 1)
        self.assertEqual(2, len(response.data['errors']))
        self.assertIn('age', response.data['errors'][0])
        self.assertIn('age', response.data['errors'][1])
        

    