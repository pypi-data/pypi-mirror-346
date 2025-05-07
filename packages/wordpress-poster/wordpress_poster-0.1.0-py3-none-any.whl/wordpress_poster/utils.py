def clean_filename(filename):
    """Clean a filename to be safe for WordPress uploads."""
    return "".join(c if c.isalnum() or c in ['-', '.'] else '-' for c in filename)
