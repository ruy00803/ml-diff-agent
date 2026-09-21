MAX_DIFF_CHARS = 15000


IMPORTANT_KEYWORDS = [
    "import",
    "feature",
    "lag",
    "rolling",
    "model",
    "params",
    "learning_rate",
    "max_depth",
    "num_leaves",
    "n_estimators",
    "epochs",
    "batch_size",
    "optimizer",
    "loss",
    "fit",
    "predict",
]


def preprocess_diff(diff_text: str) -> tuple[str, bool]:
    """
    Diffが長すぎる場合に主要な変更行を優先して抽出する。

    Returns:
        processed_diff: LLMに送るDiff
        is_trimmed: Diffを短縮したかどうか
    """

    if len(diff_text) <= MAX_DIFF_CHARS:
        return diff_text, False

    lines = diff_text.splitlines()

    important_lines = []

    for line in lines:
        lower_line = line.lower()

        if any(keyword in lower_line for keyword in IMPORTANT_KEYWORDS):
            important_lines.append(line)

    processed_diff = "\n".join(important_lines)

    if not processed_diff:
        processed_diff = diff_text[:MAX_DIFF_CHARS]

    return processed_diff[:MAX_DIFF_CHARS], True
