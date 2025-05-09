# Terrakio Admin API Client

Administrative API client for Terrakio services. This package extends the regular Terrakio API client with additional administrative capabilities.

## Features

- All features from the regular API client
- User management (create, view, edit, delete users)
- Dataset management (create, edit, update, delete datasets)

## Installation

```bash
pip install terrakio-admin-api
```

## Usage Example

```python
from terrakio_admin_api import Client

# Initialize the admin client
admin = Client(url="https://api.terrak.io", key="your-admin-api-key")

# List all users
users = admin.list_users()

# Create a new dataset
admin.create_dataset("new_dataset", bucket="my-bucket")

# List available datasets
datasets = admin.list_datasets()
```

For more documentation, see the [main repository](https://github.com/HaizeaAnalytics/terrakio-python-api). 