"""
Tests for the CLI module
"""
from dbt_docs_publisher.cli import parse_args


def test_parse_args_send_report():
    """Test parsing send-report command arguments."""
    args = parse_args([
        "send-report",
        "--profile-target", "dev",
        "--env", "dev",
        "--azure-container-name", "test-container",
        "--azure-connection-string", "test-connection-string"
    ])
    
    assert args.command == "send-report"
    assert args.profile_target == "dev"
    assert args.env == "dev"
    assert args.azure_container_name == "test-container"
    assert args.azure_connection_string == "test-connection-string"
    assert args.update_bucket_website is False


def test_parse_args_with_update_bucket_website():
    """Test parsing arguments with update-bucket-website flag."""
    args = parse_args([
        "send-report",
        "--profile-target", "dev",
        "--env", "dev",
        "--azure-container-name", "test-container",
        "--azure-connection-string", "test-connection-string",
        "--update-bucket-website"
    ])
    
    assert args.update_bucket_website is True 