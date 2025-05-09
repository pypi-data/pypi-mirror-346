# Automation Testing Framework

A comprehensive and modular Python-based testing framework for automating API, UI, database, and AWS integration tests, with robust reporting capabilities.

## 🧰 Overview

This automation framework provides a unified approach to testing various components of your application stack, including:
- API testing with request validation and response assertions
- UI testing using Playwright for browser automation
- Database testing with PostgreSQL and ClickHouse support
- AWS services integration testing
- Comprehensive reporting using Allure

## 🌟 Features

- **Modular Design**: Easily extendable for various testing needs
- **Cross-platform**: Works on any OS that supports Python
- **Reliable Reporting**: Detailed reports with Allure, including screenshots and logs
- **Environment-agnostic**: Use configuration files and environment variables for flexible deployment
- **Comprehensive Helpers**:
  - API testing with request and response validation
  - Database interactions with PostgreSQL and ClickHouse
  - AWS service interactions with S3 and more
  - Web UI automation with Playwright

## 📋 Requirements

- Python 3.11+
- Dependencies as listed in requirements.txt

## 🚀 Installation

### Via pip

```bash
pip install automation-testing-framework
```

### From source

```bash
git clone https://github.com/udisamuel/automation_framework
cd automation_framework
pip install .
```

## 🔧 Quick Start

### API Testing

```python
from automation_framework import APIHelper, APIAssert

# Create API helper
api = APIHelper(base_url="https://api.example.com")

# Make a request
response = api.get("/users")

# Assert the response
APIAssert.status_code(response, 200)
users = APIAssert.json_body(response)
print(f"Found {len(users)} users")
```

### UI Testing with Playwright

```python
from playwright.sync_api import sync_playwright
from automation_framework import BasePage, Config

# Configure the framework
Config.setup(base_url="https://example.com")

# Initialize Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # Create a base page
    base_page = BasePage(page)
    
    # Navigate to a page
    base_page.navigate_to("/login")
    
    # Interact with the page
    base_page.fill("#username", "test_user")
    base_page.fill("#password", "password123")
    base_page.click("#login-button")
    
    # Take a screenshot
    base_page.take_screenshot("login_successful")
    
    # Close the browser
    browser.close()
```

### Database Testing

```python
from automation_framework import DBHelper

# Create PostgreSQL helper (ClickHouse also supported)
db = DBHelper(
    host="localhost",
    port=5432,
    database="testdb",
    user="postgres",
    password="postgres"
)

# Execute a query
results = db.execute_query("SELECT * FROM users WHERE active = %s", (True,))

# Print results
for row in results:
    print(f"User: {row['username']}, Email: {row['email']}")

# Close the connection
db.close()
```

### AWS Integration

```python
from automation_framework import AWSHelper

# Create AWS helper
aws = AWSHelper(
    region="us-east-1",
    access_key_id="your_access_key",
    secret_access_key="your_secret_key"
)

# List S3 buckets
buckets = aws.list_buckets()
print(f"Found {len(buckets)} buckets")

# Upload a file to S3
aws.upload_file("local_file.txt", "my-bucket", "remote_file.txt")
```

## 📋 Command Line Interface

The framework includes a command-line interface for common tasks:

```bash
# Show version
automationfw --version

# Show help
automationfw --help

# Configure the framework
automationfw config --base-url "https://example.com" --timeout 30000

# List current configuration
automationfw config --list

# Make an API request
automationfw api "https://api.example.com/users" --method GET
```

## ⚙️ Configuration

You can configure the framework in several ways:

1. Environment variables
2. `.env` file (using python-dotenv)
3. Programmatically via the Config class

Example `.env` file:

```
BASE_URL=https://example.com
DEFAULT_TIMEOUT=30000
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=testdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

Programmatic configuration:

```python
from automation_framework import Config

Config.setup(
    base_url="https://example.com",
    timeout=30000,
    postgres_config={
        "host": "localhost",
        "port": 5432,
        "db": "testdb",
        "user": "postgres",
        "password": "postgres"
    }
)
```

## 📚 Documentation

For detailed documentation on all components, see the docstrings in the code or run:

```bash
# Generate HTML documentation with pdoc
pip install pdoc
pdoc --html --output-dir docs automation_framework
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
