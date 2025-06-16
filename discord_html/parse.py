import re
import yaml
from pathlib import Path

def get_config(config_file="config.yaml"):
    base_path = Path(__file__).resolve().parent
    full_path = base_path / config_file

    try:
        with open(full_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{full_path}' not found.")

def md_to_html(content: str) -> str:
    """
    Convert Discord-style markdown to HTML.
    This is a simplified version and may not cover all markdown features.
    """
    # Convert bold text
    content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
    
    # Convert italic text
    content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
    
    # Convert inline code
    content = re.sub(r'``(.*?)``', r'<code>\1</code>', content)
    
    # Convert links
    content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', content)
    
    # Convert newlines to <br>
    content = content.replace('\n', '<br>')
    
    return content

def inject(content: str, config: yaml.YAMLObject) -> str:
    for tag in config['tags']:
        content = re.sub(r'\<\')
