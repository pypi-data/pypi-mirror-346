#!/usr/bin/env python
"""
Command line interface for the automation framework.
"""

import argparse
import json
import logging
import os
import sys
from importlib.metadata import version

def setup_logging(log_level):
    """Set up logging with the specified log level."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=log_level, format=log_format)

def main():
    """Main entry point for the command line interface."""
    parser = argparse.ArgumentParser(description="Automation Testing Framework CLI")
    
    # Add version argument
    try:
        pkg_version = version("automation-testing-framework")
    except Exception:
        pkg_version = "unknown"
    
    parser.add_argument("--version", action="version", version=f"%(prog)s {pkg_version}")
    
    # Add global options
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        default="INFO", help="Set the logging level")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # 'config' command
    config_parser = subparsers.add_parser("config", help="Configure the framework")
    config_parser.add_argument("--list", action="store_true", help="List current configuration")
    config_parser.add_argument("--base-url", help="Set the base URL for API requests")
    config_parser.add_argument("--timeout", type=int, help="Set the default timeout in milliseconds")
    config_parser.add_argument("--postgres", help="Set PostgreSQL configuration (JSON string)")
    config_parser.add_argument("--clickhouse", help="Set ClickHouse configuration (JSON string)")
    config_parser.add_argument("--aws", help="Set AWS configuration (JSON string)")
    
    # 'api' command
    api_parser = subparsers.add_parser("api", help="Run API tests")
    api_parser.add_argument("url", help="URL to test")
    api_parser.add_argument("--method", choices=["GET", "POST", "PUT", "DELETE", "PATCH"],
                           default="GET", help="HTTP method")
    api_parser.add_argument("--headers", help="HTTP headers (JSON string)")
    api_parser.add_argument("--data", help="Request data (JSON string or path to file)")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(getattr(logging, args.log_level))
    
    # Handle no command
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Handle commands
    if args.command == "config":
        handle_config_command(args)
    elif args.command == "api":
        handle_api_command(args)

def handle_config_command(args):
    """Handle the 'config' command."""
    from automation_framework.config.config import Config
    
    if args.list:
        print("Current configuration:")
        print(f"  Base URL: {Config.BASE_URL}")
        print(f"  Default timeout: {Config.DEFAULT_TIMEOUT}ms")
        print("\nDatabase configuration:")
        print(f"  PostgreSQL: {Config.POSTGRES_HOST}:{Config.POSTGRES_PORT}/{Config.POSTGRES_DB}")
        print(f"  ClickHouse: {Config.CLICKHOUSE_HOST}:{Config.CLICKHOUSE_PORT}/{Config.CLICKHOUSE_DB}")
        print("\nAWS configuration:")
        print(f"  Region: {Config.AWS_REGION}")
        return
    
    # Update configuration
    postgres_config = None
    if args.postgres:
        try:
            postgres_config = json.loads(args.postgres)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format for PostgreSQL configuration")
            sys.exit(1)
    
    clickhouse_config = None
    if args.clickhouse:
        try:
            clickhouse_config = json.loads(args.clickhouse)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format for ClickHouse configuration")
            sys.exit(1)
    
    aws_config = None
    if args.aws:
        try:
            aws_config = json.loads(args.aws)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format for AWS configuration")
            sys.exit(1)
    
    Config.setup(
        base_url=args.base_url,
        timeout=args.timeout,
        postgres_config=postgres_config,
        clickhouse_config=clickhouse_config,
        aws_config=aws_config
    )
    
    print("Configuration updated successfully")

def handle_api_command(args):
    """Handle the 'api' command."""
    from automation_framework.utils.api_helper import APIHelper
    
    # Parse headers
    headers = {}
    if args.headers:
        try:
            headers = json.loads(args.headers)
        except json.JSONDecodeError:
            print("Error: Invalid JSON format for headers")
            sys.exit(1)
    
    # Parse data
    data = None
    if args.data:
        # Check if args.data is a file path
        if os.path.isfile(args.data):
            with open(args.data, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print("Error: Invalid JSON format in data file")
                    sys.exit(1)
        else:
            # Try to parse as JSON string
            try:
                data = json.loads(args.data)
            except json.JSONDecodeError:
                # If not JSON, use as raw data
                data = args.data
    
    # Create API helper and make request
    api_helper = APIHelper()
    response = api_helper.request(args.method, args.url, headers=headers, json_data=data)
    
    # Print response
    print(f"Status: {response.status_code} {response.reason}")
    print("Headers:")
    for name, value in response.headers.items():
        print(f"  {name}: {value}")
    
    print("\nBody:")
    try:
        print(json.dumps(response.json(), indent=2))
    except json.JSONDecodeError:
        print(response.text)

if __name__ == "__main__":
    main()
