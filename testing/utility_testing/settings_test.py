import pytest
from unittest.mock import patch, mock_open
from src.utility.settings_manager import Settings
import json

@pytest.fixture
def mock_data():
    return {
        "language": "French",
        "theme": "Dark",
        "institution": "Some University",
        "results_per_page": 10,
        "CRKN_url": "https://example.com",
        "database_name": "test_database.db"
    }

def test_load_settings_success(mock_data):
    mock_file_content = json.dumps(mock_data)
    with patch("builtins.open", mock_open(read_data=mock_file_content)), \
         patch("json.load", return_value=mock_data):
        settings = Settings()
        settings.load_settings()

        assert settings.language == "French"
        assert settings.theme == "Dark"
        assert settings.institution == "Some University"
        assert settings.results_per_page == 10
        assert settings.CRKN_url == "https://example.com"
        assert settings.CRKN_root_url == "https://example.com"
        assert settings.database_name == "test_database.db"

def test_load_settings_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError), \
         patch("json.load", side_effect=FileNotFoundError):
        settings = Settings()
        settings.load_settings()

        assert settings.language == "English"
        assert settings.theme == "Light"
        assert settings.institution == "Univ. of Prince Edward Island"
        assert settings.results_per_page == 25
        assert settings.CRKN_url == "https://library.upei.ca/test-page-ebooks-perpetual-access-project"
        assert settings.CRKN_root_url == "/".join(settings.CRKN_url.split("/")[:3])
        assert settings.database_name == "ebook_database.db"
