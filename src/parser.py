import json


def parse_python_file(file_bytes: bytes) -> str:
    """
    .py ファイルを UTF-8 の文字列として読み込む。
    """
    return file_bytes.decode("utf-8")


def parse_notebook_file(file_bytes: bytes) -> str:
    """
    .ipynb ファイルから code セルだけを抽出し、
    1つの文字列として返す。
    """
    notebook = json.loads(file_bytes.decode("utf-8"))

    code_cells = []

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            source = cell.get("source", [])

            if isinstance(source, list):
                code = "".join(source)
            else:
                code = source

            code_cells.append(code)

    return "\n\n".join(code_cells)


def parse_file(file_name: str, file_bytes: bytes) -> str:
    """
    拡張子に応じて適切なパーサーを呼び出す。
    """
    if file_name.endswith(".py"):
        return parse_python_file(file_bytes)

    if file_name.endswith(".ipynb"):
        return parse_notebook_file(file_bytes)

    raise ValueError("対応していないファイル形式です")