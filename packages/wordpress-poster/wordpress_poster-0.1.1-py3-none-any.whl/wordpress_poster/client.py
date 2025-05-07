import os
import requests
from dotenv import load_dotenv
from .exceptions import WordPressAuthError, WordPressUploadError, WordPressPostError
from .utils import clean_filename

load_dotenv()


class WordPressClient:
    """
    Client for interacting with the WordPress REST API.
    Loads credentials from environment variables:
      - WP_URL
      - WP_USERNAME
      - WP_PASSWORD
    """

    def __init__(self):
        self.wp_url = os.getenv("WP_URL")
        self.wp_username = os.getenv("WP_USERNAME")
        self.wp_password = os.getenv("WP_PASSWORD")
        if not all([self.wp_url, self.wp_username, self.wp_password]):
            raise WordPressAuthError("Missing WordPress credentials in environment variables.")

    def upload_image(self, image_url, meta_info=None):
        """
        Upload an image to WordPress media library.
        Args:
            image_url (str): URL of the image to upload.
            meta_info (dict): Optional dict for naming (e.g., brand, name).
        Returns:
            (bool, str|None): (success, uploaded image URL or None)
        Raises:
            WordPressUploadError on failure.
        """
        try:
            response = requests.get(image_url)
            if response.status_code != 200:
                raise WordPressUploadError(f"Failed to fetch image: {image_url}")

            # Determine file extension
            content_type = response.headers.get('content-type', '')
            ext = '.jpg'
            if 'png' in content_type:
                ext = '.png'
            elif 'webp' in content_type:
                ext = '.webp'
            elif 'jpeg' in content_type or 'jpg' in content_type:
                ext = '.jpg'

            # Create filename
            if meta_info and 'name' in meta_info:
                filename = f"{meta_info['name']}-upload{ext}".lower()
            else:
                filename = f"wordpress-upload{ext}"
            filename = clean_filename(filename)

            wp_response = requests.post(
                f"{self.wp_url}/wp-json/wp/v2/media",
                headers={"Content-Disposition": f'attachment; filename="{filename}"'},
                auth=(self.wp_username, self.wp_password),
                files={'file': (filename, response.content)},
            )

            if wp_response.status_code == 201:
                image_data = wp_response.json()
                return True, image_data['source_url'], image_data['id']
            else:
                raise WordPressUploadError(f"Image upload failed: {wp_response.text}")
        except Exception as e:
            raise WordPressUploadError(str(e))

    def create_post(self, post_type, title, content, **kwargs):
        """
        Create a new post of any type in WordPress.
        Args:
            post_type (str): e.g., 'post', 'page', or custom type.
            title (str): Post title.
            content (str): HTML content.
            **kwargs: Additional fields (slug, status, categories, meta, etc.)
        Returns:
            str|False: The post URL (link) if successful, False otherwise.
        Raises:
            WordPressPostError on failure.
        """
        post_data = {
            'title': title,
            'content': content,
        }
        post_data.update(kwargs)
        try:
            response = requests.post(
                f"{self.wp_url}/wp-json/wp/v2/{post_type}s",
                auth=(self.wp_username, self.wp_password),
                json=post_data,
            )
            if response.status_code == 201:
                post_info = response.json()
                return post_info.get('link')
            else:
                raise WordPressPostError(f"Failed to create post: {response.text}")
        except Exception as e:
            raise WordPressPostError(str(e))
