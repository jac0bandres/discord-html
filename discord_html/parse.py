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

def md_to_html(content: str, config: dict = get_config()) -> str:
    """
    Convert Discord-style markdown to HTML.
    This is a simplified version and may not cover all markdown features.
    """
    print(content)
    for r in config["regex"]:
        content = re.sub(rf'{r['pattern']}', rf'{r['match']}', content)

    print(content)
    for r in config["replace"]:
        content.replace(r['md'], r['html'])
 
    
    print(content)
    content = inject(content=content, config=config)

    print(content)
    return content

def inject(content: str, config: dict) -> str:
    for tag_config in config['tags']:
        tag_name = tag_config['tag']
        attrs = tag_config.get('attrs', {})
        attr_str = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
        pattern = rf'<{tag_name}(\s[^>]*)?>'
        def repl(match):
            return f'<{tag_name} {attr_str}>'

        content = re.sub(pattern, repl, content, flags=re.DOTALL)

    return content
