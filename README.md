# SIT Question Paper Management System

A Django-based web application for managing and accessing question papers for educational institutions.

## Features

- Department, Subject, and Question Paper organization system
- Search functionality across all content
- User-friendly interface with Bootstrap
- Secure file uploads and downloads
- Admin interface for content management

## Installation

1. Clone the repository
```
git clone <repository-url>
cd <repository-directory>
```

2. Create and activate a virtual environment
```
python -m venv venv
venv\Scripts\activate
```

3. Install the required packages
```
pip install -r requirements.txt
```

4. Run migrations
```
python manage.py migrate
```

5. Create a superuser
```
python manage.py createsuperuser
```

6. Run the development server
```
python manage.py runserver
```

7. Access the site at http://127.0.0.1:8000/qp/

## Usage

- Admin Dashboard: http://127.0.0.1:8000/admin/
- Browse question papers by department and subject
- Search for specific content using the search feature
- Download question papers as needed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 