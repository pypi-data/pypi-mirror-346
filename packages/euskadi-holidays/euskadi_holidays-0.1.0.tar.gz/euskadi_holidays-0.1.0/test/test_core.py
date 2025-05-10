from core.euskadi import EuskadiHolidays

def test_fetch():
    holidays = EuskadiHolidays(2024).get_all()
    assert isinstance(holidays, list)
