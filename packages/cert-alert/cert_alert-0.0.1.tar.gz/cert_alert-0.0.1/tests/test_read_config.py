import pytest

from src.cert_alert.config_loader import ConfigLoader


def test_valid_config(test_data_path):
    config = ConfigLoader().read_config(test_data_path / "configs/config_valid.yml")

    assert config.model_dump(exclude_none=True) == {
        "certificates": [
            {
                "name": "local test certificate",
                "file": "../tests/data/certificates/example.pem",
                "threshold": 20,
            },
            {
                "name": "github public endpoint",
                "url": "https://github.com",
                "threshold": 20,
            },
        ]
    }


def test_config_with_no_entries(test_data_path):
    with pytest.raises(Exception) as e:
        ConfigLoader().read_config(test_data_path / "configs/config_no_entries.yml")
        assert "Config validation failed" in str(e.value)


def test_config_with_invalid_entry(test_data_path):
    with pytest.raises(Exception) as e:
        ConfigLoader().read_config(test_data_path / "configs/config_invalid.yml")
        assert "Config validation failed" in str(e.value)
