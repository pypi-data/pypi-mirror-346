# wordpress_poster

A modern Python library for posting content, uploading media, and interacting with the WordPress REST API. Supports any post type, media uploads, and is designed for easy integration and automation in your projects.

## Features
- Post creation for any post type (post, page, or custom types)
- Media (image) upload
- Environment variable-based configuration
- Synchronous API
- Raises exceptions on errors
- Returns useful information (e.g., post URL, image URL)
- Simple, Pythonic interface

## Installation

**For development (recommended):**
```bash
pip install -e .
```
This will install the package in editable mode, so changes to the code are immediately reflected.

**For users (from PyPI, if published):**
```bash
pip install wordpress_poster
```

## Environment Variables
The library requires the following environment variables to be set:
- `WP_URL` — Your WordPress site URL (e.g., `https://yourblog.com`)
- `WP_USERNAME` — Your WordPress username
- `WP_PASSWORD` — Your WordPress application password (see [WordPress Application Passwords](https://wordpress.org/support/article/application-passwords/))

You can set these in your shell, or use a `.env` file in your project root:
```
WP_URL=https://yourblog.com
WP_USERNAME=yourusername
WP_PASSWORD=yourapppassword
```

## Basic Usage

### Required Fields Only
```python
from wordpress_poster.client import WordPressClient

wp = WordPressClient()

# Upload an image
success, image_url, image_id = wp.upload_image(
    'https://example.com/image.jpg',
    {'brand': 'Victor', 'name': 'Auraspeed'}
)

# Create a post (required fields only)
post_url = wp.create_post(
    post_type='post',
    title='My Title',
    content='<p>My content</p>'
)
print('Post created at:', post_url)
```

### With Optional Fields
```python
post_url = wp.create_post(
    post_type='post',
    title='My Title',
    content='<p>My content</p>',
    slug='my-title-slug',
    status='publish',
    categories=[2, 3],
    meta={'custom_field': 'value'},
    featured_media=image_id  # Set the featured image
)
print('Post created at:', post_url)
```

## Running Tests
Install dev dependencies and run tests with:
```bash
pip install -r requirements.txt
pytest
```

## Contributing
Pull requests and issues are welcome! Please open an issue if you find a bug or have a feature request.

## License
MIT License. See [LICENSE](LICENSE) for details.
