# File Downloader

A simple command-line tool to download files based on predefined file names.

## Installation

```bash
pip install dyp_file_downloader
```

## Usage

To download a file:
```bash
dyp_file_downloader --file=example1.txt
```

To specify an output directory:
```bash
dyp_file_downloader --file=example1.txt --output-dir=/path/to/directory
```

## Available Files

The following files are available for download:
- example1.txt
- example2.pdf

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Publishing

This package is configured to automatically publish to PyPI when a new release is created on GitHub. The GitHub Actions workflow will handle the build and publish process.