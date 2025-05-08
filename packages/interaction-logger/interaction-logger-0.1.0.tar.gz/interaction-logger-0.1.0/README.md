# Django Interaction Logger

A Django package for logging user activities in your web application. This package captures:
- User ID
- URL path
- Request method
- Data operations (create/read/update/delete)
- Timestamp
- IP address
- User agent
- Additional metadata

## Installation

1. Install the package from PyPI:
```bash
pip install interaction-logger
```

2. Add 'integration_logger' to your INSTALLED_APPS in settings.py:
```python
INSTALLED_APPS = [
    ...
    'integration_logger',
]
```

3. Run migrations:
```bash
python manage.py migrate integration_logger
```

## Usage

Add the middleware to your MIDDLEWARE setting in settings.py:
```python
MIDDLEWARE = [
    ...
    'integration_logger.middleware.UserActivityMiddleware',
]
```

The logger will automatically capture user activities for all requests. You can view the logs in the admin interface or query them programmatically.

## Features

- Automatic logging of user activities
- Captures HTTP methods (GET, POST, PUT, DELETE)
- Stores request data and response status
- Records IP address and user agent information
- Admin interface for viewing logs
- API endpoints for querying logs

## Development

To contribute to this project:

1. Clone the repository
2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
