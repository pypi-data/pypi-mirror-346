"""Command line interface for file downloader."""
import os
import click
import requests
from .constants import FILE_URLS

@click.command()
@click.option('--file', required=True, help='Name of the file to download')
@click.option('--output-dir', default='.', help='Directory to save the downloaded file')
def main(file: str, output_dir: str) -> None:
    """Download a file based on the file name."""
    if file not in FILE_URLS:
        click.echo(f"Error: File '{file}' not found in available files.")
        click.echo("Available files:")
        for available_file in FILE_URLS:
            click.echo(f"  - {available_file}")
        return

    url = FILE_URLS[file]
    output_path = os.path.join(output_dir, file)

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        click.echo(f"Successfully downloaded '{file}' to {output_path}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Error downloading file: {e}")
    except IOError as e:
        click.echo(f"Error saving file: {e}")

if __name__ == '__main__':
    main()