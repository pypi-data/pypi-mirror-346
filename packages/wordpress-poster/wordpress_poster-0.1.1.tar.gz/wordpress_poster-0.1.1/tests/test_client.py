import pytest
from unittest.mock import patch, Mock
from wordpress_poster.client import WordPressClient
from wordpress_poster.exceptions import WordPressUploadError, WordPressPostError


def test_client_init(monkeypatch):
    monkeypatch.setenv("WP_URL", "http://example.com")
    monkeypatch.setenv("WP_USERNAME", "user")
    monkeypatch.setenv("WP_PASSWORD", "pass")
    client = WordPressClient()
    assert client.wp_url == "http://example.com"
    assert client.wp_username == "user"
    assert client.wp_password == "pass"


def test_upload_image_success(monkeypatch):
    monkeypatch.setenv("WP_URL", "http://example.com")
    monkeypatch.setenv("WP_USERNAME", "user")
    monkeypatch.setenv("WP_PASSWORD", "pass")
    client = WordPressClient()

    # Mock requests.get and requests.post
    with patch("requests.get") as mock_get, patch("requests.post") as mock_post:
        mock_get.return_value = Mock(status_code=200, content=b"fakeimg", headers={"content-type": "image/jpeg"})
        mock_post.return_value = Mock(status_code=201, json=lambda: {"source_url": "http://example.com/img.jpg", "id": 123})
        success, url, img_id = client.upload_image("http://img", {"name": "Test"})
        assert success is True
        assert url == "http://example.com/img.jpg"
        assert img_id == 123


def test_upload_image_failure(monkeypatch):
    monkeypatch.setenv("WP_URL", "http://example.com")
    monkeypatch.setenv("WP_USERNAME", "user")
    monkeypatch.setenv("WP_PASSWORD", "pass")
    client = WordPressClient()

    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=404)
        with pytest.raises(WordPressUploadError):
            client.upload_image("http://img", {"name": "Test"})


def test_create_post_success(monkeypatch):
    monkeypatch.setenv("WP_URL", "http://example.com")
    monkeypatch.setenv("WP_USERNAME", "user")
    monkeypatch.setenv("WP_PASSWORD", "pass")
    client = WordPressClient()

    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=201, json=lambda: {"link": "http://example.com/post/1"})
        url = client.create_post("post", "title", "content")
        assert url == "http://example.com/post/1"


def test_create_post_failure(monkeypatch):
    monkeypatch.setenv("WP_URL", "http://example.com")
    monkeypatch.setenv("WP_USERNAME", "user")
    monkeypatch.setenv("WP_PASSWORD", "pass")
    client = WordPressClient()

    with patch("requests.post") as mock_post:
        mock_post.return_value = Mock(status_code=400, text="Bad request")
        with pytest.raises(WordPressPostError):
            client.create_post("post", "title", "content")
