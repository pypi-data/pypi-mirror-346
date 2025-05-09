from uxtime.res.tools import DateTimeChecker as d


def test_loc_button() -> None:
    assert d.local_utc_ux(
        '', '2025-03-18 09:36:14', 'Europe/Berlin'
    ) == ('2025-03-18 08:36:14', 1742286974)


def test_utc_button() -> None:
    assert d.utc_loc_ux(
        '', '2025-03-18 08:36:14', 'America/Montreal'
    ) == ('2025-03-18 08:36:14', 1742286974, '2025-03-18 04:36:14')


def test_ux_button() -> None:
    assert d.ux_utc_loc(
        '', '1742639404', 'Australia/Sydney'
    ) == ('2025-03-22 10:30:04', 1742639404, '2025-03-22 21:30:04')


def test_correct_dtformat_valid() -> None:
    assert d.check_dt_string('2025-03-22 10:30:04') is True


def test_incorrect_dtformat_invalid() -> None:
    # with pytest.raises(ValueError):
    assert d.check_dt_string('2025-03-22 10:30') is False
