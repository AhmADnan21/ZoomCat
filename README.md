# Selenium Test Automation for Promotion Channels

This repository contains automated tests for the Promotion Channels Configuration system.

## Setup Instructions

1. Install Python 3.9 or higher
2. Install Chrome browser
3. Install dependencies:
   ```bash
   pip install selenium pytest
   ```
4. Download ChromeDriver matching your Chrome version from: https://chromedriver.chromium.org/downloads

## Running Tests

Run the tests using:
```bash
python tests/Configure-Promotion-Channels.py
```

## Test Reports

Test reports and screenshots are saved in the `reports` directory after each test run.

## CI/CD

This project uses GitHub Actions for continuous integration. Tests run automatically on:
- Push to main branch
- Pull requests to main branch

## Project Structure

- `tests/` - Contains test scripts
- `reports/` - Contains test reports and screenshots
- `.github/workflows/` - Contains CI/CD configuration 