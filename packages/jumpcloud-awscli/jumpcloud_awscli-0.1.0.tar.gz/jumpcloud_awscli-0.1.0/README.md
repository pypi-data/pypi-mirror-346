# JumpCloud AWS CLI Authentication Utility

A Python utility for authenticating with AWS CLI using JumpCloud SAML and Device Trust certificates.

## Features

- Browser-based authentication with JumpCloud
- Automatic Device Trust certificate handling
- SAML assertion capture and parsing
- AWS STS role assumption
- AWS CLI credential configuration
- Cross-platform (works on macOS, Windows, and Linux)

## Installation

```bash
pip install jumpcloud-awscli
```

## Requirements

- Python 3.6+
- Chrome or Chromium browser
- AWS CLI installed and configured
- JumpCloud account with Device Trust certificates installed

## Usage

### Basic Usage

```bash
# Authenticate with JumpCloud and update AWS credentials
jumpcloud-aws --url "https://sso.jumpcloud.com/saml2/yourapp"
```

### All Options

```bash
jumpcloud-aws --url "https://sso.jumpcloud.com/saml2/yourapp" \
              --profile "jumpcloud" \
              --duration 43200 \
              --region "us-west-2" \
              --debug
```

### Using Environment Variables

You can set the JumpCloud URL as an environment variable:

```bash
# Set the environment variable
export JUMPCLOUD_AWS_URL="https://sso.jumpcloud.com/saml2/yourapp"

# Then you can run without the --url parameter
jumpcloud-aws
```

## How It Works

1. Launches a Chrome browser session to authenticate with JumpCloud
2. The browser automatically presents your Device Trust certificate during authentication
3. After successful authentication, it captures the SAML assertion 
4. Parses the SAML assertion to extract available AWS roles
5. Lets you select a role (if multiple are available)
6. Uses AWS STS to assume the selected role with the SAML assertion
7. Updates your AWS CLI credentials file with temporary credentials

## Troubleshooting

### Chrome/ChromeDriver Issues

If you encounter issues with Chrome or ChromeDriver:

```bash
# Reinstall the ChromeDriver dependency
pip install chromedriver-binary-auto --force-reinstall
```

### Debug Mode

For more detailed output, use the `--debug` flag:

```bash
jumpcloud-aws --url "https://sso.jumpcloud.com/saml2/yourapp" --debug
```

### Common Issues

- **Certificate selection problems**: If prompted for a certificate and it fails, check that your JumpCloud Device Trust certificate is properly installed.
- **Authentication timeouts**: If the process times out during authentication, check your network connection and ensure you're using the correct JumpCloud credentials.
- **No roles found**: Verify that your JumpCloud user has the proper AWS application role assignments.

## License

MIT License