def get_system_prompt(dataset_info, columns, numeric_cols, categorical_cols):
    """System prompt for ECharts option generation"""
    return f"""You generate ONLY valid Apache ECharts option JSON.
No explanation, no code fences, no markdown. Pure JSON only.

{dataset_info}

**Required format:**
{{
  "tooltip": {{"trigger": "axis"}},
  "xAxis": {{
    "type": "category",
    "data": df["column"].tolist()
  }},
  "yAxis": {{"type": "value"}},
  "series": [
    {{
      "name": "Series Name",
      "type": "line|bar|scatter|pie",
      "data": df["column"].tolist()
    }}
  ]
}}

Available columns: {', '.join(columns)}
Numeric: {', '.join(numeric_cols)}
Categorical: {', '.join(categorical_cols)}

Use df["column"].tolist() for data arrays.
Return ONLY the JSON option, no other text."""
