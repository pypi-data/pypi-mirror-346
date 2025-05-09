# Contributing to Traffic Cop Python SDK

Thank you for your interest in contributing to the Traffic Cop Python SDK! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please read and follow our [Code of Conduct](https://github.com/traffic-cop/traffic-cop-python-sdk/blob/main/CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip
- git

### Setting Up Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/traffic-cop-python-sdk.git
   cd traffic-cop-python-sdk
   ```
3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Code Style

We use the following tools to maintain code quality:

- [Black](https://black.readthedocs.io/en/stable/) for code formatting
- [isort](https://pycqa.github.io/isort/) for import sorting
- [mypy](https://mypy.readthedocs.io/en/stable/) for type checking

Before submitting a pull request, please run:

```bash
# Format code
black traffic_cop_client tests
isort traffic_cop_client tests

# Check types
mypy traffic_cop_client
```

### Running Tests

We use pytest for testing. To run the tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=traffic_cop_client

# Run a specific test file
pytest tests/test_client.py
```

### Documentation

Please update the documentation when you make changes to the code. This includes:

- Docstrings for new functions, classes, and methods
- Updates to the README.md if necessary
- Example code for new features

## Pull Request Process

1. Update your fork to the latest code from the main repository
2. Create a new branch for your changes
3. Make your changes and commit them with clear, descriptive commit messages
4. Run the tests to ensure they pass
5. Push your changes to your fork
6. Submit a pull request to the main repository

### Pull Request Guidelines

- Include a clear description of the changes
- Link any related issues
- Include tests for new features or bug fixes
- Ensure all tests pass
- Follow the code style guidelines

## Release Process

The maintainers will handle the release process. If you're interested in the release process, please contact the maintainers.

## Getting Help

If you need help with contributing, please:

- Open an issue on GitHub
- Contact us at support@trafficcop.ai

## License

By contributing to the Traffic Cop Python SDK, you agree that your contributions will be licensed under the project's [MIT License](https://github.com/traffic-cop/traffic-cop-python-sdk/blob/main/LICENSE).
