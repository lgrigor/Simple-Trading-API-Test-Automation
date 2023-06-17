# Trading Platform API Test Automation

This repository contains automated tests for testing [Simple-Trading-API](https://github.com/lgrigor/Simple-Trading-API)

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Test Cases](#test-cases)
- [Test Reports](#test-reports)

## Overview

The framework demonstrates pytest-based automation for testing API endpoints and WebSocket

* **Test Methods**: The framework includes multiple test methods, each responsible for testing a specific aspect of the API. These test methods contain assertions to validate the expected behavior of the API endpoints.

* **Assertions**: The assertions are used to verify the correctness of the API responses. They typically compare the actual values received from the API with the expected values. The specific assertion methods (assert) used involved comparing values, checking response codes, and validating data types.

* **Fixture and Inheritance**: The test class may inherit from other classes or fixtures that provide common setup and teardown logic, share utility functions, or establish connections to the API endpoints or databases. This allows for reusable code and helps in maintaining a modular and scalable test suite.

* **Helper Methods**: The code references several helper methods to perform common test operations such as sending requests, extracting values from responses, or performing assertions. These are used to encapsulate reusable test logic and improve code readability.

* **Markers**: The framework includes the usage of pytest markers (@pytest.mark.XYZ) to categorize and select specific tests or groups of tests for execution. These markers can be used to run tests selectively based on their purpose, tags, or attributes.

## Installation

Run locally:
  - Download the latest python `https://www.python.org/downloads/`
  - Download Jmter from `https://jmeter.apache.org/download_jmeter.cgi`
  - Set Jmeter path in [Data/main](https://github.com/lgrigor/Simple-Trading-API-Test-Automation/blob/main/Data/main.py)
  - `pip install -r requirements.txt`
  - Run in the terminal one of the suggested commands in [Usage](#usage)

Run in Docker container:
  - `docker build -t pytest-docker .`
  - `docker run pytest-docker`
    
## Usage

Test cases can be filtered using the `-m "marker"` or `-k "test_name"` options. All markers are defined in the [pytest.ini](https://github.com/lgrigor/Simple-Trading-API-Test-Automation/blob/main/pytest.ini) file.

To run the full regression, use the command: `pytest -s --html=./Results/report.html`

To run the regression without performance tests, use the command: `pytest -s -m "api_test" --html=./Results/report.html`

To run only the performance tests, use the command: `pytest -s -m "performance_test" --html=./Results/report.html`

## Test Cases

The test cases have the following properties:
* **Test Annotation**: The `@pytest.mark.api_test` annotation is used to mark the test case with a specific marker. This allows for selective test execution or filtering based on markers.

* **Test Fixture**: The test method is defined as a function within a test class. The class contains test fixtures or setup methods to prepare the test environment before executing each test case.
  
* **Test Assertions**: The test method contains multiple assertions using the assert statement. Each assertion verifies a specific condition or expected behavior of the system under test. These assertions are used to validate the response received after calling the send_post_order method.
  
* **Test Data**: The test method provides specific test data. This allows for testing different scenarios and inputs to cover a range of test cases.

## Test Reports

The test report is generated bt pytest-html which is a pytest plugin that generates detailed HTML reports for test results. It provides a visually appealing way to view and analyze the test execution summary, individual test outcomes, and associated metadata.

Example is here - [report.html](https://github.com/lgrigor/Simple-Trading-API-Test-Automation/blob/main/Results). Download and open html file with browser.

