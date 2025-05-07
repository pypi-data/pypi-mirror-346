class WordPressPosterError(Exception):
    """Base exception for wordpress_poster library."""

    pass


class WordPressAuthError(WordPressPosterError):
    """Raised when authentication with WordPress fails."""

    pass


class WordPressUploadError(WordPressPosterError):
    """Raised when media upload fails."""

    pass


class WordPressPostError(WordPressPosterError):
    """Raised when post creation or update fails."""

    pass
