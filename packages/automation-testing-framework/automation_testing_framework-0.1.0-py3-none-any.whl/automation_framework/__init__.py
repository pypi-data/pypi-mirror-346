"""
Automation Testing Framework
============================

A comprehensive and modular Python-based testing framework for automating API, UI, 
database, and AWS integration tests, with robust reporting capabilities.

This package provides utilities for:
- API testing with request validation and response assertions
- UI testing using Playwright for browser automation
- Database testing with PostgreSQL and ClickHouse support
- AWS services integration testing
- Comprehensive reporting using Allure

For more information, see https://github.com/udisamuel/automation_framework
"""

__version__ = "0.1.0"

# Import the main components to expose them at package level
from automation_framework.utils.api_helper import APIHelper, APIAssert
from automation_framework.utils.db_helper import DBHelper
from automation_framework.utils.aws_helper import AWSHelper
from automation_framework.utils.playwright_wrapper import PlaywrightWrapper
from automation_framework.pages.base_page import BasePage
