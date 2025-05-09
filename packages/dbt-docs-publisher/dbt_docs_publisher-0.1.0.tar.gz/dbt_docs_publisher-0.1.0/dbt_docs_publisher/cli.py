"""
Command-line interface for dbt-docs-publisher
"""
import argparse
import sys
from . import __version__
from .uploader import run_send_report


def parse_args(args=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        prog="ddp",
        description="dbt docs publisher - Upload dbt documentation to Azure"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    # send-report command
    send_report_parser = subparsers.add_parser(
        "send-report",
        help="Generate and upload dbt documentation"
    )
    
    send_report_parser.add_argument(
        "--profile-target",
        help="The dbt profile target to use",
        required=True
    )
    
    send_report_parser.add_argument(
        "--env",
        help="Environment (dev, prod, etc.)",
        required=True
    )
    
    send_report_parser.add_argument(
        "--azure-container-name",
        help="Azure Blob Storage container name",
        required=True
    )
    
    send_report_parser.add_argument(
        "--azure-connection-string",
        help="Azure Blob Storage connection string",
        required=True
    )
    
    send_report_parser.add_argument(
        "--update-bucket-website",
        action="store_true",
        help="Display information about enabling static website hosting"
    )
    
    parsed_args = parser.parse_args(args)
    if not parsed_args.command:
        parser.print_help()
        sys.exit(1)
        
    return parsed_args


def main(args=None):
    """Main entry point for the CLI."""
    args = parse_args(args)
    
    if args.command == "send-report":
        return run_send_report(
            profile_target=args.profile_target,
            env=args.env,
            container_name=args.azure_container_name,
            connection_string=args.azure_connection_string,
            update_bucket_website=args.update_bucket_website
        )
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 