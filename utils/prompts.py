# Deprecated: Use prompts module instead
from prompts import vegalite_prompt, plotly_prompt, echarts_prompt


def get_vegalite_prompt(dataset_info, numeric_cols, categorical_cols):
    """System prompt for Vega-Lite spec generation"""
    return vegalite_prompt.get_system_prompt(dataset_info, numeric_cols, categorical_cols)


def get_plotly_prompt(dataset_info, columns, numeric_cols, categorical_cols):
    """System prompt for Plotly spec generation"""
    return plotly_prompt.get_system_prompt(dataset_info, columns, numeric_cols, categorical_cols)


def get_echarts_prompt(dataset_info, columns, numeric_cols, categorical_cols):
    """System prompt for ECharts option generation"""
    return echarts_prompt.get_system_prompt(dataset_info, columns, numeric_cols, categorical_cols)
