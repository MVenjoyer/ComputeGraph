## CompGraph

A Python library for performing operations on graphs, including external sorting, graph traversals, and customizable
operations. This project is designed with modularity and scalability in mind, featuring robust unit testing and coverage
checks to ensure reliability.

### Getting Started

These instructions will help you set up the project on your local machine for development, testing, or general usage.

### Prerequisites

Ensure you have the following installed:

* Python 3.8 or later
* pip for managing Python dependencies
* Virtual environment tools like venv or virtualenv
* Recommended Python Packages

1. pytest - for running unit tests
2. pytest-cov - for measuring test coverage

### Installing

A step-by-step guide to setting up the project:

* Clone the repository:

* Set up a virtual environment:

* Install dependencies:

```
pip install -r requirements.txt

```

* Check installation by running tests:

```
pytest tests
```

### Running the Tests

This project includes automated tests for ensuring correctness, memory efficiency, and adherence to coding style.

#### Sample Tests

The following are covered in the test suite:

#### Correctness Tests:

Validate the correctness of implemented algorithms and operations. Example:

```
pytest tests/correctness
```

#### Memory Tests:

Evaluate memory usage during graph operations. Example:

```
pytest tests/memory
```

#### Custom Tests:

Verify additional user-defined scenarios. Example:

```
pytest tests/my_tests
```

#### Style Tests

Check that the code adheres to best practices and consistent styling:

```
flake8 compgraph
```
