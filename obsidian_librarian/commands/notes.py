import click
import os
from pathlib import Path
import base64
import requests
from ..config import get_config

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_image_with_gpt4v(image_path, note_name):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")

    base64_image = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Please write detailed notes about {note_name}. Transcribe the content from the image faithfully, and then organize that information in an appropriate way. Format the response in markdown."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4096
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    return response.json()['choices'][0]['message']['content']

def get_matching_notes(vault_path, prefix):
    """Get all notes that start with the given prefix"""
    if not vault_path or not os.path.exists(vault_path):
        return []
    
    all_files = os.listdir(vault_path)
    matching_notes = [f[:-3] for f in all_files 
                     if f.endswith('.md') and 
                     f.startswith(prefix)]
    return matching_notes

@click.group()
def notes():
    """Note manipulation commands"""
    pass

@notes.command()
def format():
    """Format individual notes"""
    click.echo("Formatting notes...")

@notes.command()
def fill():
    """Complete partial notes"""
    click.echo("Filling notes...")

@notes.command()
@click.argument('note_name', type=click.STRING, autocompletion=get_matching_notes)
def ocr(note_name):
    """Convert screenshots to text"""
    config = get_config()
    vault_path = config.get('vault_path')
    
    if not vault_path:
        click.echo("Error: Vault path not configured")
        return

    note_path = Path(vault_path) / f"{note_name}.md"
    if not note_path.exists():
        click.echo(f"Error: Note {note_name} not found")
        return

    # Find all images in the note's directory
    note_dir = note_path.parent
    image_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    images = [f for f in note_dir.glob(f"{note_name}.*") if f.suffix.lower() in image_extensions]

    if not images:
        click.echo("No images found for this note")
        return

    for image_path in images:
        click.echo(f"Processing image: {image_path}")
        try:
            content = process_image_with_gpt4v(str(image_path), note_name)
            
            # Create new markdown file with OCR results
            output_path = note_dir / f"{note_name}_ocr.md"
            with open(output_path, 'w') as f:
                f.write(content)
            
            click.echo(f"OCR results saved to: {output_path}")
        except Exception as e:
            click.echo(f"Error processing image: {e}")
