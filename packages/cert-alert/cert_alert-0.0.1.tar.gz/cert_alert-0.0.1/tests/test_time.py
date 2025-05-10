from datetime import datetime, timedelta

from cert_alert.cert_alert import CertAlert

FIVE_DAY_THRESHOLD = timedelta(days=5)


def test_six_days_until_expiry():
    # rigged now time
    now = datetime(1970, 1, 3)

    # rigged expiry time
    expiry = datetime(1970, 1, 10)

    assert CertAlert.check_threshold_reached(FIVE_DAY_THRESHOLD, now, expiry) == (
        False,
        7,
    )


def test_five_days_until_expiry():
    # rigged now time
    now = datetime(1970, 1, 4)

    # rigged expiry time
    expiry = datetime(1970, 1, 10)

    assert CertAlert.check_threshold_reached(FIVE_DAY_THRESHOLD, now, expiry) == (
        False,
        6,
    )


def test_one_day_until_expiry():
    # rigged now time
    now = datetime(1970, 1, 9)

    # rigged expiry time
    expiry = datetime(1970, 1, 10)

    assert CertAlert.check_threshold_reached(FIVE_DAY_THRESHOLD, now, expiry) == (
        True,
        1,
    )


def test_one_day_expired():
    # rigged now time
    now = datetime(1970, 1, 11)

    # rigged expiry time
    expiry = datetime(1970, 1, 10)

    assert CertAlert.check_threshold_reached(FIVE_DAY_THRESHOLD, now, expiry) == (
        True,
        -1,
    )
