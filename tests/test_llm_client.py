from types import SimpleNamespace
from unittest.mock import MagicMock

import httpx
import pytest
from google.genai import errors
from src import llm_client


@pytest.fixture
def client(monkeypatch):
    factory = MagicMock()
    monkeypatch.setattr(llm_client.genai, "Client", factory)
    instance = factory.return_value.__enter__.return_value
    instance.models.generate_content.return_value = SimpleNamespace(text="変更点")
    return instance


def test_success_and_model_override(client, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    assert llm_client.analyze_diff("+x=1", api_key="test", model="test-model") == "変更点"
    kwargs = client.models.generate_content.call_args.kwargs
    assert kwargs["model"] == "test-model"
    assert "+x=1" in kwargs["contents"]


def test_missing_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(llm_client.AnalysisError, match="GEMINI_API_KEY"):
        llm_client.analyze_diff("diff")


@pytest.mark.parametrize("code, message", [(400, "設定"), (401, "無効"),
    (403, "権限"), (404, "モデル"), (429, "上限"), (503, "再試行")])
def test_api_errors(client, code, message):
    client.models.generate_content.side_effect = errors.APIError(code, {"error": {"message": "private detail"}})
    with pytest.raises(llm_client.AnalysisError, match=message) as exc:
        llm_client.analyze_diff("diff", api_key="test")
    assert "private detail" not in str(exc.value)


@pytest.mark.parametrize("value", [None, "", "  "])
def test_empty_response(client, value):
    client.models.generate_content.return_value.text = value
    with pytest.raises(llm_client.AnalysisError, match="空"):
        llm_client.analyze_diff("diff", api_key="test")


def test_transport_error(client):
    client.models.generate_content.side_effect = httpx.ConnectError("private detail")
    with pytest.raises(llm_client.AnalysisError, match="通信状態"):
        llm_client.analyze_diff("diff", api_key="test")


def test_environment_model(client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test")
    monkeypatch.setenv("GEMINI_MODEL", "configured-model")
    llm_client.analyze_diff("diff")
    assert client.models.generate_content.call_args.kwargs["model"] == "configured-model"
