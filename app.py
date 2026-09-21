import os

import streamlit as st

from src.parser import parse_file
from src.diff_engine import generate_diff
from src.diff_preprocessor import preprocess_diff
from src.llm_client import AnalysisError, analyze_diff


def setting(name):
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets.get(name)
    except FileNotFoundError:
        return None


def main():
    st.title("ML Experiment Diff Agent")
    st.write("機械学習実験のコード差分を比較し、変更内容をAIが整理します。")
    col1, col2 = st.columns(2)
    with col1:
        base = st.file_uploader("Base Experiment", type=["py", "ipynb"])
    with col2:
        target = st.file_uploader("Target Experiment", type=["py", "ipynb"])
    if base is None or target is None:
        st.info("BaseとTargetの両方のファイルを選択してください。")
        return
    try:
        diff = generate_diff(parse_file(base.name, base.getvalue()),
                             parse_file(target.name, target.getvalue()))
    except (ValueError, UnicodeError):
        st.error("ファイルを読み込めません。UTF-8のPythonファイル、または正しいNotebookを選択してください。")
        return
    if not diff:
        st.success("コード上の差分はありません。")
        return
    processed, trimmed = preprocess_diff(diff)
    with st.expander("Raw Diff（全差分）", expanded=True):
        st.code(diff, language="diff")
    if trimmed:
        st.warning("差分が大きいため、AI分析では主要な変更箇所を優先しています。")
    with st.expander("Geminiへ送信する差分"):
        st.code(processed, language="diff")
    st.caption("「AIで分析」を押すと、上記の送信対象の差分をGemini APIへ送信します。")
    if st.button("AIで分析", type="primary"):
        try:
            with st.spinner("差分を分析しています…"):
                report = analyze_diff(processed, api_key=setting("GEMINI_API_KEY"),
                                      model=setting("GEMINI_MODEL"))
            st.subheader("分析結果")
            st.markdown(report)
        except AnalysisError as exc:
            st.error(str(exc))
        except Exception:
            st.error("予期しないエラーが発生しました。設定とインストール環境を確認してください。")


if __name__ == "__main__":
    main()
