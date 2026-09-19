from src.diff_preprocessor import preprocess_diff


def test_preprocess_diff_short():
    diff_text = "-x = 1\n+x = 2"

    processed_diff, is_trimmed = preprocess_diff(diff_text)

    assert processed_diff == diff_text
    assert is_trimmed is False


def test_preprocess_diff_long():
    diff_text = "a" * 16000 + "\n+learning_rate = 0.01"

    processed_diff, is_trimmed = preprocess_diff(diff_text)

    assert is_trimmed is True
    assert "learning_rate" in processed_diff