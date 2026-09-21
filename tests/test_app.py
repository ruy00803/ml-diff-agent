from io import BytesIO
from pathlib import Path
from unittest.mock import Mock

from streamlit.testing.v1 import AppTest
import streamlit as st
from src import llm_client

APP = Path(__file__).resolve().parents[1] / "app.py"


def setup_uploads(monkeypatch, base=b'x=1', target=b'x=2', name='test.py'):
    def upload(label, **kwargs):
        file = BytesIO(base if label == "Base Experiment" else target)
        file.name = name
        return file
    monkeypatch.setattr(st, "file_uploader", upload)


def test_preview_does_not_send_and_click_sends(monkeypatch):
    setup_uploads(monkeypatch)
    analyze = Mock(return_value="テスト結果")
    monkeypatch.setattr(llm_client, "analyze_diff", analyze)
    app = AppTest.from_file(str(APP)).run()
    assert not app.exception
    assert len(app.code) == 2
    analyze.assert_not_called()
    app.button[0].click().run()
    analyze.assert_called_once()
    assert any(x.value == "テスト結果" for x in app.markdown)
    assert not app.exception


def test_invalid_notebook_shows_error(monkeypatch):
    setup_uploads(monkeypatch, base=b'[]', name='test.ipynb')
    app = AppTest.from_file(str(APP)).run()
    assert app.error
    assert not app.button
    assert not app.exception


def test_no_diff_does_not_offer_analysis(monkeypatch):
    setup_uploads(monkeypatch, target=b'x=1')
    app = AppTest.from_file(str(APP)).run()
    assert app.success
    assert not app.button
    assert not app.exception
