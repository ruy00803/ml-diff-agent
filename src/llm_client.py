import os
from pathlib import Path

from google import genai


def get_client():
    """
    Gemini APIクライアントを作成する。
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません")

    return genai.Client(api_key=api_key)


def load_prompt() -> str:
    """
    prompts/diff_analysis_prompt.txt を読み込む。
    """
    prompt_path = Path("prompts/diff_analysis_prompt.txt")

    return prompt_path.read_text(encoding="utf-8")


def analyze_diff(diff_text: str) -> str:
    """
    コード差分をGeminiに渡し、
    分析結果を文字列で返す。
    """
    client = get_client()

    prompt_template = load_prompt()

    prompt = prompt_template.format(
        diff_text=diff_text
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text