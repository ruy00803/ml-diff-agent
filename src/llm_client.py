import os
from pathlib import Path

from google import genai
from google.genai import errors
import httpx

DEFAULT_MODEL = "gemini-3.6-flash"
PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts/diff_analysis_prompt.txt"


class AnalysisError(Exception):
    """利用者に表示できる分析エラー。"""


def load_prompt() -> str:
    return PROMPT_PATH.read_text(encoding="utf-8")


def analyze_diff(diff_text: str, *, api_key: str | None = None,
                 model: str | None = None) -> str:
    api_key = api_key or os.getenv("GEMINI_API_KEY")
    model = model or os.getenv("GEMINI_MODEL") or DEFAULT_MODEL
    if not api_key:
        raise AnalysisError("GEMINI_API_KEYを環境変数またはStreamlit Secretsに設定してください。")
    try:
        with genai.Client(api_key=api_key, http_options={"timeout": 60000}) as client:
            response = client.models.generate_content(
                model=model,
                contents=load_prompt().format(diff_text=diff_text),
            )
    except errors.APIError as exc:
        messages = {
            400: "APIキー・モデル名・リクエスト設定を確認してください。",
            401: "APIキーが無効です。設定を確認してください。",
            403: "APIキーまたはモデルの利用権限を確認してください。",
            404: "モデルが見つかりません。GEMINI_MODELの設定を確認してください。",
            429: "APIの利用上限に達しました。割り当てを確認し、時間をおいて再試行してください。",
        }
        raise AnalysisError(messages.get(exc.code, "Gemini APIでエラーが発生しました。時間をおいて再試行してください。")) from exc
    except httpx.TransportError as exc:
        raise AnalysisError("Gemini APIに接続できませんでした。通信状態を確認して再試行してください。") from exc
    if not response.text or not response.text.strip():
        raise AnalysisError("分析結果が空でした。入力内容を確認して再試行してください。")
    return response.text
