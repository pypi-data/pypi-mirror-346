# Bugster-framework

Bugster is a comprehensive testing and debugging framework designed to streamline end-to-end testing with Playwright. It provides a robust infrastructure for test automation, authentication handling, and detailed test reporting.

## Features

- **Playwright Integration**: Built on top of Playwright for reliable browser automation
- **Flexible Authentication**: Support for multiple authentication strategies and credential management
- **Advanced Test Runner**: Custom pytest plugin with dependency management between tests
- **Comprehensive Reporting**: Automated screenshots, traces, and detailed test reports
- **Mouse and Keyboard Simulation**: Enhanced input simulation with visual feedback
- **Test Metadata Management**: Centralized configuration for test environments and settings

## Installation

```language=bash
# Install using pip
pip install bugster

# Or if using Poetry
poetry add bugster
```

## Usage

### Basic Test Setup

```language=python
import pytest
from bugster.core.bugster_expect import expect

def test_login_flow(page):
    # Navigate to login page
    page.goto("/login")
    
    # Fill login form
    page.get_by_placeholder("Email").fill("user@example.com")
    page.get_by_placeholder("Password").fill("password")
    page.get_by_role("button", name="Sign In").click()
    
    # Verify successful login
    expect(page.get_by_text("Welcome")).to_be_visible()
```

### Authentication Strategies

Bugster supports flexible authentication methods:

```language=python
from bugster.auth import UserInputLoginStrategy

# Define login steps
login_instructions = [
    {"action": "goto", "url": "/auth/sign-in"},
    {"action": "fill", "method": "placeholder", "value": "email", "text": "{email}"},
    {"action": "fill", "method": "placeholder", "value": "password", "text": "{password}"},
    {"action": "click", "method": "role", "value": "button", "kwargs": {"name": "Sign In"}}
]

# Create login strategy
auth_strategy = UserInputLoginStrategy(login_instructions)
```

### Test Dependencies

```language=python
@pytest.mark.depends(on=["test_login"])
def test_dashboard(page):
    # This test will only run if test_login passes
    page.goto("/dashboard")
    expect(page.get_by_text("Dashboard")).to_be_visible()
```

### Trace Capture

```language=python
from bugster.reporting.trace_viewer import start_trace, stop_and_save_trace

def test_with_trace(page, context):
    # Start recording trace
    start_trace(context)
    
    # Test steps...
    
    # Save trace for debugging
    trace_path = stop_and_save_trace(context, "my_test")
    print(f"Trace saved to: {trace_path}")
```

## Configuration

Bugster uses a JSON configuration file for test settings:

```language=json
{
  "settings": {
    "browser": "chromium",
    "headless": true,
    "viewport": {"width": 1920, "height": 1080}
  },
  "environment": {
    "dev": {
      "base_url": "https://dev.example.com",
      "auth_url": "https://dev.example.com/login"
    },
    "prod": {
      "base_url": "https://example.com",
      "auth_url": "https://example.com/login"
    }
  },
  "auth": {
    "credentials": [
      {
        "id": "admin",
        "email": "admin@example.com",
        "password": "admin_password"
      },
      {
        "id": "user",
        "email": "user@example.com",
        "password": "user_password"
      }
    ],
    "instructions": [
      {"action": "goto", "url": "/login"},
      {"action": "fill", "method": "placeholder", "value": "email", "text": "{email}"},
      {"action": "fill", "method": "placeholder", "value": "password", "text": "{password}"},
      {"action": "click", "method": "role", "value": "button", "kwargs": {"name": "Sign In"}}
    ]
  }
}
```

## Running Tests

```language=bash
# Run tests with specific environment
pytest --env=dev

# Specify Bugster directory for credentials and reports
pytest --bugster-dir=/path/to/bugster
```


## Contributing

We welcome contributions to Bugster! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) file for details on how to contribute.

## License

Bugster is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Changelog

See the [CHANGELOG.md](CHANGELOG.md) file for details on what has changed in each version of Bugster.

## Support

If you encounter any issues or have questions, please file an issue on the [GitHub issue tracker](https://github.com/yourusername/bugster/issues).

## Acknowledgements

Bugster is built on top of the excellent [Playwright](https://playwright.dev/) and [pytest](https://docs.pytest.org/) projects. We're grateful to the maintainers and contributors of these projects for their fantastic work.
