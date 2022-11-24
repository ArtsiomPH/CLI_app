from main import get_result_dict


def test_send_list_with_none():
    res = get_result_dict([None])
    assert res == "There were no urls among the strings"


def test_send_list_with_dicts():
    dicts_list = [
        {"site_1": {"GET": 200, "HEAD": 200}},
        {"site_2": {"GET": 200, "OPTIONS": 404}},
    ]
    res = get_result_dict(dicts_list)
    assert res == {
        "site_1": {"GET": 200, "HEAD": 200},
        "site_2": {"GET": 200, "OPTIONS": 404},
    }


def test_send_list_with_dict_and_none():
    dicts_list = [
        {"site_1": {"GET": 200, "HEAD": 200}},
        None,
        {"site_2": {"GET": 200, "OPTIONS": 404}},
    ]
    res = get_result_dict(dicts_list)
    assert res == {
        "site_1": {"GET": 200, "HEAD": 200},
        "site_2": {"GET": 200, "OPTIONS": 404},
    }
