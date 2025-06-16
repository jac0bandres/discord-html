import discord_html
import inspect
import actions
import asyncio

dispatch_map = {
    "md_to_html": discord_html.md_to_html,
    "fetch_messages_by_id": actions.fetch_messages_by_id,
}

def dispatch(func_name: str, *args, **kwargs):
    if func_name not in dispatch_map:
        raise ValueError(f"Dispatcher failed, no function mapped for '{func_name}]")
        
    return dispatch_map[func_name](*args, **kwargs)
