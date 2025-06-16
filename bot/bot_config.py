''' 
bot_config.py
Parses command line arguments using the editable config.yaml file.

'''
from pathlib import Path
import yaml

def open_config_file(file_name: str = "config.yaml"):
    base_path = Path(__file__).resolve().parent
    full_path = base_path / file_name
    try:
        with open(full_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{full_path}' not found.")

def get_flags(flag_definitions: list[dict]):
    flag_map = {}
    for flag_def in flag_definitions:
        flag_map[flag_def["name"]] = flag_def
        for alias in flag_def["aliases"]:
            flag_map[alias] = flag_def

    return flag_map

def parse_input(flag_map: dict, input_str: str):
    print(flag_map)
    split_flags = input_str.strip().split()
    args = {}

    for f in split_flags:
        flag = flag_map[f]

        if flag is None:
            raise ValueError(f"Unknown argument {f}")

        if flag['type'] == 'bool':
            args[flag['name']] = True
            continue

        if flag['type'] == 'string':
            arg = split_flags[split_flags.index(f) + 1] if split_flags.index(f) + 1 < len(split_flags) else None
            if arg is None or arg.startswith('-'):
                raise ValueError(f'''
                Missing value for argument: {f}\n
                {flag['name']}\t{flag['aliases']}\n
                {flag['required']}\n
                {flag['description']}\n
                ''')

            args[flag['name']] = arg

    return args
