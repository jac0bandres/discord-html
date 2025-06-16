''' 
config.py
Parses command line arguments using the editable config.yaml file.

'''

import yaml
def open_config_file(file_path: str = "./config.yaml"):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")

def parse_input(flag_definitions, input_str):
    split_flags = input_str.strip().split()
    args = {}

    for f in split_flags:
        flag = flag_definitions.get(f)
        if flag is None:
            raise ValueError(f"Unknown argument: {f}")

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
