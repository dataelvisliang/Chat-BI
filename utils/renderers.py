import json
import streamlit as st


def render_plotly_chart(spec_json, df):
    """Render Plotly chart from JSON spec"""
    import plotly.graph_objects as go
    import re

    # Replace df references with actual values BEFORE parsing JSON
    def replace_df_refs(match):
        expr = match.group(0)
        try:
            result = eval(expr, {"df": df})
            return json.dumps(result)
        except:
            return expr

    # Find and replace all df["..."].tolist() or df['...'].tolist() patterns
    spec_json = re.sub(r'df\[["\'][^"\']+["\']\]\.tolist\(\)', replace_df_refs, spec_json)

    spec = json.loads(spec_json)
    fig = go.Figure(spec)
    st.plotly_chart(fig, use_container_width=True)


def render_echarts_chart(spec_json, df):
    """Render ECharts chart from JSON option"""
    from streamlit_echarts import st_echarts
    import re

    # Replace df references with actual values BEFORE parsing JSON
    def replace_df_refs(match):
        expr = match.group(0)
        try:
            result = eval(expr, {"df": df})
            return json.dumps(result)
        except Exception as e:
            return expr

    # Find and replace all df["..."].tolist() or df['...'].tolist() patterns
    spec_json = re.sub(r'df\[["\'][^"\']+["\']\]\.tolist\(\)', replace_df_refs, spec_json)

    option = json.loads(spec_json)
    st_echarts(options=option, height="500px")
