from src.diff_engine import generate_diff


def test_generate_diff_no_change():
    base_code = "x = 1"
    target_code = "x = 1"

    result = generate_diff(base_code, target_code)

    assert result == ""


def test_generate_diff_value_change():
    base_code = "learning_rate = 0.05"
    target_code = "learning_rate = 0.01"

    result = generate_diff(base_code, target_code)

    assert "-learning_rate = 0.05" in result
    assert "+learning_rate = 0.01" in result


def test_generate_diff_added_line():
    base_code = "x = 1"
    target_code = "x = 1\ny = 2"

    result = generate_diff(base_code, target_code)

    assert "+y = 2" in result