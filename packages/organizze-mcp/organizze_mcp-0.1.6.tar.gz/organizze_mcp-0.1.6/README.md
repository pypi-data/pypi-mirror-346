# Organizze MCP

A Python-based integration for Organizze financial management platform using FastMCP.

## Description

This project provides a Multi-Call Protocol (MCP) server for the Organizze financial management platform, allowing operations like viewing transactions and managing categories.

## Features

- List transactions within a date range
- List available categories
- Set categories for transactions

## Installation

This project uses Poetry for dependency management.

```bash
# Clone the repository
git clone https://github.com/yourusername/organizze-mcp.git
cd organizze-mcp

# Install dependencies
poetry install
```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
ORGANIZZE_EMAIL=your_organizze_email
ORGANIZZE_TOKEN=your_organizze_api_token
```

You can obtain your API token from your Organizze account settings.

## Usage

Run the MCP server:

```bash
poetry run python src/organizze-mcp/main.py
```

## Requirements

- Python 3.12+
- fastmcp 2.3.3+
- requests 2.32.3+

## License

[Add your license here]

## Author

Diego (dccarbone@gmail.com) 