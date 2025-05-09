# this file is responsible for installing the package

from setuptools import find_packages, setup

from sensitive_data_detector.version import __version__

setup(
    # Basic Info
    name="sensitive_data_detector",
    version=__version__,
    author="Akash Anandani",
    author_email="akashanandani.56@gmail.com",
    # Package Structure
    packages=find_packages(exclude=["tests", "tests.*", "docs", "docs.*"]),
    # Dependencies
    install_requires=[
        # No runtime dependencies needed
    ],
    python_requires=">=3.11",
    # Development Dependencies
    extras_require={
        "dev": [
            "pytest>=8.3.5",
            "pytest-cov",  # for test coverage
            "black",  # for code formatting
            "flake8",  # for linting
            "mypy",  # for type checking
        ]
    },
    # Test Configuration
    test_suite="tests",
    tests_require=["pytest>=8.3.5"],
    # Documentation
    description="A package to detect sensitive information in code and files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # License
    license="MIT",
    # Project URLs
    url="https://github.com/akashdv25/sensitive_info_detector",
    project_urls={
        "Bug Tracker": "https://github.com/akashdv25/sensitive_info_detector/issues",
    },
    # Classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "Topic :: Software Development :: Testing",
        "Operating System :: OS Independent",
    ],
    # Package Data
    package_data={
        "sensitive_data_detector": [
            "config.json",
        ],
    },
    include_package_data=True,
)
