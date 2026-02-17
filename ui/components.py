import streamlit as st


def render_metric_cards(metrics, columns=3):
    for i in range(0, len(metrics), columns):
        cols = st.columns(columns)
        row = metrics[i:i + columns]
        for idx, metric in enumerate(row):
            with cols[idx]:
                st.markdown(
                    f"""
                    <div class="card">
                        <div class="card-title">{metric["label"]}</div>
                        <div class="card-value">{metric["value"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)
