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
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        description='JumpCloud AWS CLI SAML Authentication',
        prog='jumpcloud-awscli'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'jumpcloud-awscli {__version__}'
    )

    # Create subparsers
    subparsers = parser.add_subparsers(dest='command')

    # Create the 'login' command
    login_parser = subparsers.add_parser(
        'login',
        help='Authenticate with JumpCloud and obtain AWS credentials'
    )

    # Check for default URL in environment
    default_url = os.environ.get("JUMPCLOUD_AWS_URL", "https://sso.jumpcloud.com/saml2/prodigal-aws")

    # Add arguments to the login command
    login_parser.add_argument(
        '--url',
        default=default_url,
        help='JumpCloud SSO URL for AWS (can also set JUMPCLOUD_AWS_URL env var)'
    )
    login_parser.add_argument(
        '--profile',
        default='default',
        help='AWS profile to update (default: default)'
    )
    login_parser.add_argument(
        '--duration',
        type=int,
        default=43100,
        help='Session duration in seconds (default: 43100)'
    )
    login_parser.add_argument(
        '--region',
        default='us-east-2',
        help='AWS region (default: us-east-2)'
    )
    login_parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )

    # Parse arguments
    args = parser.parse_args()

    # If no command is provided, show help
    if not args.command:
        # For backward compatibility, check if --url is provided as a top-level argument
        if len(sys.argv) > 1 and sys.argv[1].startswith('--'):
            # If top-level arguments are used, assume 'login' command
            print("Note: It is recommended to use 'jumpcloud-awscli login' instead of direct options.")
            login_args = parser.parse_args(['login'] + sys.argv[1:])
            return handle_login(login_args)
        else:
            parser.print_help()
            sys.exit(1)

    # Handle commands
    if args.command == 'login':
        return handle_login(args)


def handle_login(args):
    """
    Handle the login command.

    Args:
        args: Parsed command-line arguments

    Returns:
        int: Exit code
    """
    # Check if URL is provided
    if not args.url:
        print(
            "\nError: JumpCloud SSO URL is required. Please provide it with --url or set JUMPCLOUD_AWS_URL environment variable.")
        print("\nUsage: jumpcloud-awscli login --url https://sso.jumpcloud.com/saml2/your-app\n")
        return 1

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
        return 0
    else:
        print("\nAuthentication failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())