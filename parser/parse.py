import re

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
    
    return f"<p>{content}</p>"
