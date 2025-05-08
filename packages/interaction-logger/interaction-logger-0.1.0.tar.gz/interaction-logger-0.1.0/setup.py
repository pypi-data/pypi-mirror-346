from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
with open(os.path.join('integration_logger', '__init__.py'), 'r', encoding='utf-8') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="interaction-logger",
    version=version,
    author="Josphat-n",
    author_email="josphatnjoroge254@gmail.com",  # Replace with actual email
    description="A package for logging user interactions with a django distributed system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="django, logging, user activity, audit trail, monitoring",
    python_requires=">=3.10",
    install_requires=[
        "Django>=4.2.0",
        "django-user-agents>=0.4.0",
        "python-json-logger>=2.0.7"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-django>=4.5.0",
            "black>=23.0.0",
            "isort>=5.10.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "coverage>=7.0.0",
        ],
    },
    license="MIT"  
)
