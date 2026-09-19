import streamlit as st

from src.parser import parse_file
from src.diff_engine import generate_diff
from src.diff_preprocessor import preprocess_diff
from src.llm_client import analyze_diff


st.title("ML Experiment Diff Agent")

st.write(
    "Kaggleや機械学習実験のコード差分を比較し、"
    "変更内容をAIが整理します。"
)


col1, col2 = st.columns(2)

with col1:
    base_file = st.file_uploader(
        "Base Experiment",
        type=["py", "ipynb"]
    )

with col2:
    target_file = st.file_uploader(
        "Target Experiment",
        type=["py", "ipynb"]
    )


if st.button("実験差分を解析"):

    if base_file is None or target_file is None:
        st.warning("BaseとTargetの両方のファイルを選択してください。")

    else:
        base_code = parse_file(
            base_file.name,
            base_file.getvalue()
        )

        target_code = parse_file(
            target_file.name,
            target_file.getvalue()
        )

        diff_text = generate_diff(
            base_code,
            target_code
        )

        if not diff_text:
            st.success("コード上の差分はありません。")

        else:
            processed_diff, is_trimmed = preprocess_diff(diff_text)

            if is_trimmed:
                st.warning(
                    "差分が大きいため、AI分析では主要な変更箇所を優先しています。"
                )

            try:
                report = analyze_diff(processed_diff)

                st.subheader("📊 分析結果")
                st.markdown(report)

            except Exception:
                st.error(
                    "AI分析に失敗しました。"
                    "Gemini APIが一時的に混雑している可能性があります。"
                )

            with st.expander("Raw Diff"):
                st.code(diff_text, language="diff")