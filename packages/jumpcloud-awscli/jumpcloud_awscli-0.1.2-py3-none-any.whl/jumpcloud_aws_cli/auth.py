#!/usr/bin/env python3
"""
Authentication module for JumpCloud AWS CLI integration.

This module handles the browser-based authentication with JumpCloud,
SAML assertion capture, and AWS credential generation.
"""

import base64
import configparser
import json
import os
import time
import urllib.parse
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, parse_qs

import boto3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException


class JumpCloudAWSAuth:
    """
    Class for handling JumpCloud AWS authentication with Device Trust certificates.

    This class manages the browser session for JumpCloud authentication,
    SAML assertion extraction, AWS role selection, and credential generation.
    """

    def __init__(self, jumpcloud_url, profile="default", duration=3600, region="us-east-1", debug=False):
        """
        Initialize the authentication class with JumpCloud and AWS configuration.

        Args:
            jumpcloud_url (str): JumpCloud SSO URL for AWS
            profile (str): AWS CLI profile name to update
            duration (int): Session duration in seconds
            region (str): AWS region for credential generation
            debug (bool): Enable debug logging
        """
        self.jumpcloud_url = jumpcloud_url
        self.profile = profile
        self.duration = duration
        self.region = region
        self.debug = debug
        self.aws_credentials_file = os.path.expanduser("~/.aws/credentials")

        # Ensure AWS credentials directory exists
        os.makedirs(os.path.dirname(self.aws_credentials_file), exist_ok=True)

        if self.debug:
            print(f"Debug mode enabled")
            print(f"Using JumpCloud URL: {self.jumpcloud_url}")
            print(f"AWS profile: {self.profile}")
            print(f"Session duration: {self.duration} seconds")
            print(f"AWS region: {self.region}")

    def get_saml_assertion(self):
        """
        Launch a Chrome browser to authenticate with JumpCloud and retrieve the SAML assertion.
        The browser will automatically present the Device Trust certificate.

        Returns:
            str: Base64-encoded SAML assertion or None if unsuccessful
        """
        print("Launching browser for JumpCloud authentication...")

        # Configure Chrome options
        chrome_options = Options()
        # Uncomment the line below to run headless (no visible browser)
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Remove automation info bar
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Add network interception to capture SAML requests
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        # Initialize Chrome driver with fallback to webdriver-manager if needed
        driver = None
        try:
            # Try the standard approach first
            driver = webdriver.Chrome(options=chrome_options)
            if self.debug:
                print("Successfully initialized Chrome driver")
        except WebDriverException:
            # Fallback to webdriver-manager if available
            try:
                if self.debug:
                    print("Standard Chrome driver failed, trying webdriver-manager...")

                try:
                    # Try to import webdriver-manager
                    from webdriver_manager.chrome import ChromeDriverManager
                    service = Service(ChromeDriverManager().install())
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    if self.debug:
                        print("Successfully initialized Chrome driver using webdriver-manager")
                except ImportError:
                    print("webdriver-manager not found. Please install it with: pip install webdriver-manager")
                    print("or install the package with: pip install jumpcloud-awscli[auto-webdriver]")
                    return None
            except Exception as e:
                print(f"Failed to initialize Chrome driver with webdriver-manager: {e}")
                print("Please ensure Chrome is installed and ChromeDriver is available in your PATH.")
                print("You can install ChromeDriver manually or install webdriver-manager:")
                print("  pip install webdriver-manager")
                return None

        if not driver:
            print("Failed to initialize Chrome driver.")
            return None

        try:
            # Navigate to JumpCloud SSO URL
            if self.debug:
                print(f"Navigating to: {self.jumpcloud_url}")

            driver.get(self.jumpcloud_url)

            # Wait for authentication to complete and redirect to AWS console
            print("Waiting for authentication to complete...")
            WebDriverWait(driver, 60).until(
                EC.url_contains("aws.amazon.com/")
            )

            if self.debug:
                print(f"Redirected to: {driver.current_url}")

            # Wait a moment for the redirect to fully complete
            time.sleep(3)

            # AWS SSO Flow: Check if we're in the AWS console without capturing the SAML assertion
            if "console.aws.amazon.com" in driver.current_url:
                print("Successfully authenticated and redirected to AWS Console.")
                print("Checking browser logs for SAML assertion...")

                # Extract SAML assertion from browser logs
                saml_assertion = self.extract_saml_from_logs(driver)
                if saml_assertion:
                    if self.debug:
                        print("Found SAML assertion in browser logs")
                    return saml_assertion

                # If we can't find it in logs, we need to modify our approach
                print("SAML assertion not found in browser logs.")
                print("Initiating alternative SAML capture method...")

                # Navigate to AWS federation endpoint to capture SAML
                if self.debug:
                    print("Navigating to AWS SAML endpoint")
                driver.get("https://signin.aws.amazon.com/saml")

                # Wait for SAML form to appear
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "SAMLResponse"))
                    )

                    # Find SAML assertion in the form
                    saml_input = driver.find_element(By.NAME, "SAMLResponse")
                    if saml_input.get_attribute("value"):
                        if self.debug:
                            print("Found SAML assertion in SAML endpoint form")
                        return saml_input.get_attribute("value")
                except Exception as e:
                    if self.debug:
                        print(f"Error waiting for SAML form: {e}")

            # Original SAML detection flow for backward compatibility
            if "saml" in driver.current_url:
                # Parse SAML from URL
                parsed_url = urlparse(driver.current_url)
                params = parse_qs(parsed_url.query)
                if "SAMLResponse" in params:
                    if self.debug:
                        print("Found SAML assertion in URL parameters")
                    return params["SAMLResponse"][0]

            # Check for SAML form in the page
            soup = BeautifulSoup(driver.page_source, "html.parser")
            saml_input = soup.find("input", {"name": "SAMLResponse"})

            if saml_input:
                saml_assertion = saml_input.get("value")
                if self.debug:
                    print("Found SAML assertion in page form")
                return saml_assertion
            else:
                print("Failed to find SAML assertion in the browser response.")
                print("Current URL:", driver.current_url)

                # Last resort: Ask the user to manually capture SAML
                print("\nAlternative method required. Please follow these steps:")
                print("1. In your browser window that just opened, go to: https://signin.aws.amazon.com/saml")
                print("2. You should be redirected to a page with a SAML response")
                print("3. If asked to authenticate again, please do so")

                input("Press Enter when ready to continue...")

                # Check again for SAML response
                if "signin.aws.amazon.com/saml" in driver.current_url:
                    soup = BeautifulSoup(driver.page_source, "html.parser")
                    saml_input = soup.find("input", {"name": "SAMLResponse"})
                    if saml_input:
                        if self.debug:
                            print("Found SAML assertion after manual intervention")
                        return saml_input.get("value")

                return None
        except Exception as e:
            print(f"Error during browser authentication: {e}")
            return None
        finally:
            # Close the browser
            driver.quit()

    def extract_saml_from_logs(self, driver):
        """
        Extract SAML assertion from browser performance logs.
        This is used when direct SAML form access is not available.

        Args:
            driver: Selenium WebDriver instance

        Returns:
            str: Base64-encoded SAML assertion or None if not found
        """
        if self.debug:
            print("Extracting SAML from browser logs")

        logs = driver.get_log('performance')

        for log in logs:
            if 'message' not in log:
                continue

            log_entry = json.loads(log['message'])

            # Look for network requests with SAML data
            if (
                    'message' in log_entry
                    and 'method' in log_entry['message']
                    and log_entry['message']['method'] == 'Network.requestWillBeSent'
            ):
                request = log_entry['message'].get('params', {}).get('request', {})
                url = request.get('url', '')

                # Check for SAML in POST data
                if 'SAMLResponse' in url or 'saml' in url.lower():
                    post_data = request.get('postData', '')
                    if 'SAMLResponse=' in post_data:
                        # Extract and decode SAML response
                        saml_parts = post_data.split('SAMLResponse=')[1].split('&')[0]
                        return urllib.parse.unquote(saml_parts)

        return None

    def get_aws_roles(self, saml_assertion):
        """
        Parse the SAML assertion to extract available AWS roles.

        Args:
            saml_assertion (str): Base64-encoded SAML assertion

        Returns:
            list: Available AWS roles from the SAML assertion
        """
        # Decode SAML assertion from base64
        saml_xml = base64.b64decode(saml_assertion)
        root = ET.fromstring(saml_xml)

        # Find SAML attribute with role info
        role_attribute = "https://aws.amazon.com/SAML/Attributes/Role"
        roles = []

        # Namespaces used in SAML XML
        ns = {
            'saml2': 'urn:oasis:names:tc:SAML:2.0:assertion',
            'saml2p': 'urn:oasis:names:tc:SAML:2.0:protocol'
        }

        # Extract role attributes
        for attribute in root.findall(f".//saml2:Attribute[@Name='{role_attribute}']", ns):
            for value in attribute.findall(".//saml2:AttributeValue", ns):
                roles.append(value.text)

        if self.debug:
            print(f"Found {len(roles)} AWS roles in SAML assertion")
            for role in roles:
                print(f"  - {role}")

        return roles

    def select_role(self, roles):
        """
        Let user select an AWS role if multiple roles are available.

        Args:
            roles (list): Available AWS roles

        Returns:
            tuple: (role_arn, principal_arn) pair or None if selection fails
        """
        if not roles:
            print("No AWS roles found in the SAML assertion.")
            return None

        # Parse role ARNs
        role_pairs = []
        for role in roles:
            parts = role.split(',')
            if len(parts) == 2:
                role_arn = parts[0] if "role" in parts[0].lower() else parts[1]
                principal_arn = parts[1] if "role" in parts[0].lower() else parts[0]
                role_pairs.append((role_arn, principal_arn))

        # If only one role, return it
        if len(role_pairs) == 1:
            if self.debug:
                print(f"Only one role available, selecting automatically: {role_pairs[0][0]}")
            return role_pairs[0]

        # Otherwise, let user select a role
        print("\nAvailable AWS roles:")
        for i, (role_arn, _) in enumerate(role_pairs):
            # Extract the role name from the ARN for better readability
            role_name = role_arn.split('/')[-1] if '/' in role_arn else role_arn
            print(f"[{i}] {role_name}")

        selection = input("\nSelect a role (number): ")
        try:
            index = int(selection)
            selected_role = role_pairs[index]
            if self.debug:
                print(f"Selected role: {selected_role[0]}")
            return selected_role
        except (ValueError, IndexError):
            print("Invalid selection.")
            return None

    def assume_role_with_saml(self, saml_assertion, role_arn, principal_arn):
        """
        Use AWS STS to assume role with SAML assertion.

        Args:
            saml_assertion (str): Base64-encoded SAML assertion
            role_arn (str): AWS IAM role ARN to assume
            principal_arn (str): AWS IAM principal ARN

        Returns:
            dict: AWS credentials or None if assumption fails
        """
        if self.debug:
            print(f"Assuming role {role_arn} with principal {principal_arn}")
            print(f"Session duration: {self.duration} seconds")

        sts_client = boto3.client('sts', region_name=self.region)

        try:
            response = sts_client.assume_role_with_saml(
                RoleArn=role_arn,
                PrincipalArn=principal_arn,
                SAMLAssertion=saml_assertion,
                DurationSeconds=self.duration
            )

            if self.debug:
                print("Successfully assumed role")
                expiration = response['Credentials']['Expiration']
                print(f"Credentials expire at: {expiration}")

            return {
                'AccessKeyId': response['Credentials']['AccessKeyId'],
                'SecretAccessKey': response['Credentials']['SecretAccessKey'],
                'SessionToken': response['Credentials']['SessionToken'],
                'Expiration': response['Credentials']['Expiration']
            }
        except Exception as e:
            print(f"Error assuming role: {e}")
            return None

    def update_aws_credentials(self, credentials):
        """
        Update AWS credentials file with temporary credentials.

        Args:
            credentials (dict): AWS credentials to store

        Returns:
            None
        """
        if self.debug:
            print(f"Updating AWS credentials file: {self.aws_credentials_file}")
            print(f"Profile: {self.profile}")

        config = configparser.ConfigParser()

        # Read existing config if it exists
        if os.path.exists(self.aws_credentials_file):
            config.read(self.aws_credentials_file)

        # Create or update profile section
        if not config.has_section(self.profile):
            config.add_section(self.profile)

        # Update credentials
        config[self.profile]['aws_access_key_id'] = credentials['AccessKeyId']
        config[self.profile]['aws_secret_access_key'] = credentials['SecretAccessKey']
        config[self.profile]['aws_session_token'] = credentials['SessionToken']
        config[self.profile]['region'] = self.region

        # Save the config file
        with open(self.aws_credentials_file, 'w') as configfile:
            config.write(configfile)

        # Friendly output
        print(f"\nAWS temporary credentials updated in profile '{self.profile}'")
        expiration = credentials['Expiration'].strftime('%Y-%m-%d %H:%M:%S')
        print(f"Credentials will expire on: {expiration}")

    def authenticate(self):
        """
        Main authentication flow:
        1. Get SAML assertion from JumpCloud via browser
        2. Extract available AWS roles
        3. Let user select role if multiple are available
        4. Assume the role using STS and SAML assertion
        5. Update AWS credentials file

        Returns:
            bool: True if authentication was successful, False otherwise
        """
        # Get SAML assertion
        saml_assertion = self.get_saml_assertion()
        if not saml_assertion:
            print("Failed to get SAML assertion from JumpCloud.")
            return False

        # Get available roles
        roles = self.get_aws_roles(saml_assertion)

        # Select role
        role_principal_pair = self.select_role(roles)
        if not role_principal_pair:
            return False

        role_arn, principal_arn = role_principal_pair
        print(f"\nAssuming role: {role_arn}")

        # Assume role
        credentials = self.assume_role_with_saml(saml_assertion, role_arn, principal_arn)
        if not credentials:
            return False

        # Update credentials file
        self.update_aws_credentials(credentials)
        return True