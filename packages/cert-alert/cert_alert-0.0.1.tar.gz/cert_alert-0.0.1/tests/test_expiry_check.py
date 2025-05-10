from datetime import datetime, timedelta, timezone

from cert_alert.cert_alert import CertAlert


def test_check_threshold_reached_with_pem_files(test_data_path):
    now = datetime.now(timezone.utc)

    cert_path = test_data_path / "certificates/dynamic/expired_30days_ago.pem"
    expiry = CertAlert().get_expiry_from_pem(cert_path)
    assert CertAlert().check_threshold_reached(timedelta(days=30), now, expiry) == (
        True,
        -31,
    )
    assert CertAlert().check_threshold_reached(timedelta(days=1), now, expiry) == (
        True,
        -31,
    )

    cert_path = test_data_path / "certificates/dynamic/expired_365days_ago.pem"
    expiry = CertAlert().get_expiry_from_pem(cert_path)
    assert CertAlert().check_threshold_reached(timedelta(days=30), now, expiry) == (
        True,
        -366,
    )
    assert CertAlert().check_threshold_reached(timedelta(days=1), now, expiry) == (
        True,
        -366,
    )

    cert_path = test_data_path / "certificates/dynamic/valid_30days.pem"
    expiry = CertAlert().get_expiry_from_pem(cert_path)
    assert CertAlert().check_threshold_reached(timedelta(days=1), now, expiry) == (
        False,
        29,
    )
    assert CertAlert().check_threshold_reached(timedelta(days=29), now, expiry) == (
        False,
        29,
    )
    assert CertAlert().check_threshold_reached(timedelta(days=30), now, expiry) == (
        True,
        29,
    )
    assert CertAlert().check_threshold_reached(timedelta(days=31), now, expiry) == (
        True,
        29,
    )

    cert_path = test_data_path / "certificates/dynamic/valid_365days.pem"
    expiry = CertAlert().get_expiry_from_pem(cert_path)
    assert CertAlert().check_threshold_reached(timedelta(days=1), now, expiry) == (
        False,
        364,
    )
    assert CertAlert().check_threshold_reached(timedelta(days=364), now, expiry) == (
        False,
        364,
    )
    assert CertAlert().check_threshold_reached(timedelta(days=365), now, expiry) == (
        True,
        364,
    )
    assert CertAlert().check_threshold_reached(timedelta(days=366), now, expiry) == (
        True,
        364,
    )
