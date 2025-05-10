from datetime import datetime
import pytest

from cert_alert.cert_alert import CertAlert


def test_extract_expiry(test_data_path):
    expiry = CertAlert().get_expiry_from_pem(
        test_data_path / "certificates/dynamic/valid_365days.pem"
    )

    assert type(expiry) is datetime


def test_extraction_attempt_from_non_existing_file(test_data_path):
    with pytest.raises(Exception) as e:
        CertAlert().get_expiry_from_pem(test_data_path / "non_existing.pem")

    assert "Certificate" in str(e.value) and "not found" in str(e.value)


def test_extraction_attempt_from_broken_file(test_data_path):
    with pytest.raises(Exception) as e:
        CertAlert().get_expiry_from_pem(test_data_path / "certificates/broken.pem")

    assert "Failed to read certificate" in str(e.value)


def test_extract_expiry_from_url():
    expiry = CertAlert().get_expiry_from_url("https://github.com")

    assert type(expiry) is datetime


def test_extract_expiry_from_invalid_url():
    with pytest.raises(Exception) as e:
        CertAlert().get_expiry_from_url("invalid_url")

    assert "Failed to read certificate from url" in str(e.value)
