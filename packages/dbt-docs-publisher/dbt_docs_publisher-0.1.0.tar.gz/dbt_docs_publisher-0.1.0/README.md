# dbt-docs-publisher

A CLI tool for publishing dbt documentation to Azure Blob Storage.

## Features

- Automatically runs `dbt docs generate --static`
- Finds generated docs in temp directories
- Uploads all documentation files to Azure Blob Storage
- Organizes files by environment (dev, prod, etc.)
- Provides info on enabling static website hosting in Azure

## Installation

```bash
pip install dbt-docs-publisher
```

For use in Databricks:

```bash
pip install dbt-docs-publisher[databricks]
```

## Usage

```bash
ddp send-report \
  --profile-target=dev \
  --env=dev \
  --azure-container-name=dbt-docs \
  --azure-connection-string="your_azure_connection_string" \
  --update-bucket-website
```

### Arguments

- `--profile-target`: The dbt profile target to use
- `--env`: Environment name (dev, prod, etc.) - used for organizing files in storage
- `--azure-container-name`: Azure Blob Storage container name
- `--azure-connection-string`: Azure Blob Storage connection string
- `--update-bucket-website`: (Optional) Display information about enabling static website hosting

## Using in Databricks

Add to your Databricks job:

```yaml
libraries:
  - pypi:
      package: dbt-docs-publisher[databricks]
commands:
  - ddp send-report --profile-target=${bundle.target} --env=prod --azure-container-name=dbt-docs --azure-connection-string="$dl_conn_str"
```

## Development

### Setup

```bash
git clone https://github.com/yourusername/dbt-docs-publisher.git
cd dbt-docs-publisher
pip install -e ".[dev]"
```

### Building and Publishing

```bash
# Build the package
python setup.py sdist bdist_wheel

# Publish to PyPI
twine upload dist/*
```

## License

MIT 