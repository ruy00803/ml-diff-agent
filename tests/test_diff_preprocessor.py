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

def test_keyword_heavy_diff_is_bounded():
    from src.diff_preprocessor import MAX_DIFF_CHARS
    processed, trimmed = preprocess_diff('+model.fit(x)\n' * 3000)
    assert trimmed
    assert len(processed) <= MAX_DIFF_CHARS
