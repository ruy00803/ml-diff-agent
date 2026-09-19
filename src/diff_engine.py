import difflib


def generate_diff(base_code: str, target_code: str) -> str:
    """
    BaseコードとTargetコードを比較し、
    Unified Diff形式の文字列を返す。
    """

    base_lines = base_code.splitlines()
    target_lines = target_code.splitlines()

    diff = difflib.unified_diff(
        base_lines,
        target_lines,
        fromfile="base",
        tofile="target",
        lineterm=""
    )

    return "\n".join(diff)