#!/usr/bin/env python3
"""
Command-line interface for JumpCloud AWS CLI Authentication.

This module provides the command-line entry point for the JumpCloud AWS CLI
authentication utility.
"""

import argparse
import sys
import os
from .auth import JumpCloudAWSAuth
from . import __version__


def main():
    """
    Main entry point for the CLI.

    Parse command-line arguments and run the authentication flow.
    """
    # Check for default URL in environment
    default_url = os.environ.get("JUMPCLOUD_AWS_URL", "")

    parser = argparse.ArgumentParser(description='JumpCloud AWS CLI SAML Authentication')
    parser.add_argument('--url', default="https://sso.jumpcloud.com/saml2/prodigal-aws",
                        help='JumpCloud SSO URL for AWS (can also set JUMPCLOUD_AWS_URL env var)')
    parser.add_argument('--profile', default='default',
                        help='AWS profile to update (default: default)')
    parser.add_argument('--duration', type=int, default=43100,
                        help='Session duration in seconds (default: 43100)')
    parser.add_argument('--region', default='us-east-2',
                        help='AWS region (default: us-east-2)')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug logging')
    parser.add_argument('--version', action='store_true',
                        help='Show version and exit')

    args = parser.parse_args()

    # Handle version request
    if args.version:
        print(f"jumpcloud-awscli version {__version__}")
        sys.exit(0)

    # Check if URL is provided
    if not args.url:
        parser.print_help()
        print(
            "\nError: JumpCloud SSO URL is required. Please provide it with --url or set JUMPCLOUD_AWS_URL environment variable.")
        sys.exit(1)

    auth = JumpCloudAWSAuth(
        jumpcloud_url=args.url,
        profile=args.profile,
        duration=args.duration,
        region=args.region,
        debug=args.debug
    )

    if auth.authenticate():
        print("\nAuthentication successful! You can now use AWS CLI commands.")
        print(f"Example: aws --profile {args.profile} s3 ls")
    else:
        print("\nAuthentication failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()