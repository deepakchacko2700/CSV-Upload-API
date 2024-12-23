# CSV Upload API

API to upload csv file containing users data. API processes, validates and saved users in the database and response with saved and rejected users count and errors that caused the rejection.

## API End Point

POST /upload/

This endpoint allows you to upload a CSV file for processing.

- URL: http://127.0.0.1:8000/upload/ (locally)

- Method: POST

- Content-Type: multipart/form-data

#### CSV File Format and Data Validation Rules
csv file should contain 3 columns.
- name (Must be a non-empty string)
- email (Must be a unique and valid email address)
- age (Must be an integer between 0 and 120)

## Usage
#### Upload the CSV File Using Postman

1. **Open Postman**.
2. Set the HTTP method to **POST**.
3. Set the **URL** to `http://127.0.0.1:8000/upload/`.
4. Under the **Body** tab, select **form-data**.
5. Set the **key** to `file` (this is the expected name for the file field).
6. Select the **file** you want to upload (make sure it is a `.csv` file).
7. Click **Send**.

#### Upload the CSV File Using cURL

You can also upload the CSV file using cURL from the command line:
```bash
curl -X POST -F "file=@/path/to/your/file.csv" http://127.0.0.1:8000/upload/
```

Replace /path/to/your/file.csv with the path to your CSV file.

## Runnung the project locally
1. Clone the repository:
```bash
git clone https://github.com/deepakchacko2700/CSV-Upload-API.git

cd <your-project-directory>
```
2. Create a python virtual environement
```python
python -m venv <virtualenv name>
```
3. Install packages and dependencies
```python
pip install -r requirements.txt
```

4. Apply migrations to create the necessary database tables:
```python
python manage.py migrate
```
5. Run the Django development server:
```python
python manage.py runserver
```
6. Your API will now be available at http://127.0.0.1:8000/. You can use tools like Postman or cURL to upload CSV files to the /api/upload/ endpoint.

