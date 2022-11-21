from main import validate_string


def test_send_correct_url():
    res = validate_string('https://google.com')
    assert res is True


def test_send_url_with_no_schema():
    res = validate_string('google.com')
    assert res is False


def test_send_random_string():
    res = validate_string('some string')
    assert res is False


def test_send_empty_string():
    res = validate_string('')
    assert res is False
