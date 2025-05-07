import pytest
from wordpress_poster.exceptions import (
    WordPressPosterError,
    WordPressAuthError,
    WordPressUploadError,
    WordPressPostError,
)

def test_base_exception():
    with pytest.raises(WordPressPosterError):
        raise WordPressPosterError("base error")

def test_auth_exception():
    with pytest.raises(WordPressAuthError):
        raise WordPressAuthError("auth error")

def test_upload_exception():
    with pytest.raises(WordPressUploadError):
        raise WordPressUploadError("upload error")

def test_post_exception():
    with pytest.raises(WordPressPostError):
        raise WordPressPostError("post error") 