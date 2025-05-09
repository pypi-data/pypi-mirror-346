from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the requirements file
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="automation-testing-framework",
    version="0.1.0",
    author="Udi Samuel",
    author_email="udisamuel@example.com",
    description="A comprehensive and modular Python-based testing framework for automating API, UI, database, and AWS integration tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/udisamuel/automation_framework",
    project_urls={
        "Bug Tracker": "https://github.com/udisamuel/automation_framework/issues",
        "Documentation": "https://github.com/udisamuel/automation_framework/docs",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "Framework :: Pytest",
    ],
    packages=find_packages(exclude=["tests*", ".venv", ".git", ".github", ".idea", ".pytest_cache"]),
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "automationfw=automation_framework.cli:main",
        ],
    },
)
