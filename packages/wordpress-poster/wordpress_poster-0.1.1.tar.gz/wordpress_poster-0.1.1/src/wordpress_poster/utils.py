import string

def clean_filename(filename):
    """Clean a filename to be safe for WordPress uploads (ASCII only)."""
    allowed = set(string.ascii_letters + string.digits + '-.')
    return ''.join(c if c in allowed else '-' for c in filename)
