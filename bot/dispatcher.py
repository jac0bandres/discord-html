import discord_html
import bot_config 

dispatch_map = {
    "md_to_html": discord_html.md_to_html
}

def dispatch(func_name: str, *args, **kwargs):
    if func_name not in dispatch_map:
        raise ValueError(f"Dispatcher failed, no function mapped for '{func_name}]")
    return dispatch_map[func_name](*args, **kwargs)
