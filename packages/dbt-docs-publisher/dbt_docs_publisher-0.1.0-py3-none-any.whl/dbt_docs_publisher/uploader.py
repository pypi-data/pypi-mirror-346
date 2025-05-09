"""
Upload dbt documentation to Azure Blob Storage
"""
import glob
import os
import subprocess
import sys
from pathlib import Path
from azure.storage.blob import BlobServiceClient, ContentSettings


def find_target_directory():
    """Find the most recent dbt target directory."""
    target_dirs = glob.glob("/tmp/tmp-dbt-run-*/target")
    
    if not target_dirs:
        print("❌ No dbt target directory found in /tmp/tmp-dbt-run-*/target")
        sys.exit(1)
    
    # Sort by modification time (newest first)
    latest_dir = max(target_dirs, key=os.path.getmtime)
    return latest_dir


def upload_files_to_azure(
    target_dir, container_name, connection_string, env
):
    """Upload files to Azure Blob Storage."""
    print(f"⏳ Uploading files to Azure container: {container_name}")
    
    try:
        # Create the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )
        
        # Get container client
        container_client = blob_service_client.get_container_client(
            container_name
        )
        
        # Create container if it doesn't exist
        if not container_client.exists():
            print(f"📦 Creating container {container_name}")
            container_client.create_container()

        # Path prefix for the environment
        env_prefix = f"{env}/"
        
        # Upload all files from the target directory
        target_path = Path(target_dir)
        
        file_count = 0
        for file_path in target_path.glob("**/*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(target_path)
                # Create blob name with environment prefix
                blob_name = f"{env_prefix}{relative_path}"
                
                # Determine content type
                content_type = "text/html"
                if file_path.suffix == ".css":
                    content_type = "text/css"
                elif file_path.suffix == ".js":
                    content_type = "application/javascript"
                elif file_path.suffix in [".png", ".jpg", ".jpeg", ".gif"]:
                    content_type = f"image/{file_path.suffix.lstrip('.')}"
                
                # Upload to Azure
                with open(file_path, "rb") as data:
                    container_client.upload_blob(
                        name=blob_name,
                        data=data,
                        overwrite=True,
                        content_settings=ContentSettings(
                            content_type=content_type
                        )
                    )
                    file_count += 1
        
        msg = f"✅ Successfully uploaded {file_count} files to {container_name}"
        print(msg)
        
        # Return the base URL for the container
        account_name = blob_service_client.account_name
        base_url = (
            f"https://{account_name}.blob.core.windows.net/"
            f"{container_name}/{env}/"
        )
        return base_url
        
    except Exception as e:
        print(f"❌ Error uploading to Azure: {str(e)}")
        sys.exit(1)


def run_dbt_docs_generate(profile_target):
    """Run dbt docs generate command."""
    print(f"⏳ Running dbt docs generate with target {profile_target}")
    
    try:
        subprocess.run(
            ["dbt", "docs", "generate", "--target", profile_target, 
             "--static"],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ Successfully generated dbt docs")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating dbt docs: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ dbt command not found. Is dbt installed?")
        sys.exit(1)


def run_send_report(
    profile_target, env, container_name, connection_string, 
    update_bucket_website
):
    """
    Generate dbt docs and upload to Azure Blob Storage.
    
    Args:
        profile_target: dbt profile target
        env: Environment (dev, prod, etc.)
        container_name: Azure container name
        connection_string: Azure connection string
        update_bucket_website: Whether to show static website hosting info
    """
    # Step 1: Run dbt docs generate
    run_dbt_docs_generate(profile_target)
    
    # Step 2: Find the target directory
    target_dir = find_target_directory()
    print(f"📁 Found dbt docs in: {target_dir}")
    
    # Step 3: Upload to Azure
    base_url = upload_files_to_azure(
        target_dir, container_name, connection_string, env
    )
    
    # Step 4: Display website info if requested
    if update_bucket_website:
        print("\n📋 Static Website Hosting Information:")
        print("To enable static website hosting in Azure Storage:")
        print("1. Go to the Azure Portal")
        print("2. Navigate to your storage account")
        print("3. Click on 'Static website' under 'Settings'")
        print("4. Set 'Static website' to 'Enabled'")
        print(f"5. Set 'Index document name' to '{env}/index.html'")
        print("6. Click 'Save'")
    
    print(f"\n🌐 Your dbt docs are available at: {base_url}index.html")
    return 0 