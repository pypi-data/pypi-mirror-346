# tests/test_sensitive_check.py
import pytest

from sensitive_data_detector.sensitive_check import has_sensitive_info


# Test data fixtures
@pytest.fixture
def sample_files(tmp_path):
    """Create sample files for testing

    The name sample_files in the test function refers to whatever the fixture function returns
    thats why we are using it in the test functions instead of using files['___']
    hence , In the test, we use the fixture name to access whatever the fixture returned

    tmp_path is a pytest fixture that automatically creates a temporary directory for each test
    it is used to create files and directories in the test directory

    """
    files = {}  # dict to store the file paths

    # add test case for api key
    api_key_file = tmp_path / "api_key.txt"
    api_key_file.write_text("api_key : 'sk_test_1234567890'")
    files["api_key"] = str(api_key_file)

    # File with email
    email_file = tmp_path / "email.txt"
    email_file.write_text("Contact: test@example.com")
    files["email"] = str(email_file)

    # test case when everything is clean
    clean_file = tmp_path / "clean.txt"
    clean_file.write_text("Hello world")
    files["clean"] = str(clean_file)

    return files


# Basic tests
def test_has_sensitive_info_email(sample_files):
    """Test email detection"""
    result = has_sensitive_info(sample_files["email"])
    assert result is True


def test_has_sensitive_info_api_key(sample_files):
    """Test api key detection"""
    result = has_sensitive_info(sample_files["api_key"])
    assert result is True


def test_has_sensitive_info_clean(sample_files):
    """Test clean file"""
    result = has_sensitive_info(sample_files["clean"])
    assert result is False


# Error cases
def test_has_sensitive_info_file_not_found():
    """Test non-existent file"""
    with pytest.raises(FileNotFoundError):
        has_sensitive_info("nonexistent_file.txt")


# edge case
def test_has_sensitive_info_empty_file(tmp_path):
    """Test empty file"""
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")
    result = has_sensitive_info(str(empty_file))
    assert result is False
