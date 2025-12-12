import json
import streamlit as st
import pandas as pd
import re


def evaluate_python_expressions(spec_json, df):
    """
    Flexibly evaluate ANY Python expression containing df or pd in JSON.
    Works with complex operations like filtering, date parsing, groupby, etc.

    Uses regex to find expression boundaries and a tokenizer for proper nesting.
    """

    def scan_for_tolist_end(text, start_pos):
        """
        Scan forward from start_pos to find the end of expression ending with .tolist() variants.
        Properly tracks nesting to handle expressions like:
        df[pd.to_datetime(...).dt.period() == ...].groupby(...).count().index.tolist()

        The start_pos should point to the start of the df/pd identifier.
        We track depth RELATIVE to that starting point.
        """
        i = start_pos
        paren_depth = 0
        bracket_depth = 0
        in_string = None
        started = False  # Track if we've opened any brackets/parens

        while i < len(text):
            char = text[i]

            # Handle string literals (skip escaped quotes)
            if char in ('"', "'") and (i == 0 or text[i-1] != '\\'):
                if in_string is None:
                    in_string = char
                elif in_string == char:
                    in_string = None
                i += 1
                continue

            # Only process syntax outside of strings
            if in_string is None:
                # Track bracket/paren depth
                if char == '(':
                    paren_depth += 1
                    started = True
                elif char == ')':
                    paren_depth -= 1
                elif char == '[':
                    bracket_depth += 1
                    started = True
                elif char == ']':
                    bracket_depth -= 1

                # Once we've started tracking AND we're back to depth 0, look for .tolist() endings
                if started and paren_depth == 0 and bracket_depth == 0:
                    # Check all variants of tolist endings (check longest first to avoid partial matches)
                    if i >= 15 and text[i-15:i+1] == '.values.tolist()':
                        # Verify no chaining continues after this
                        if i + 1 >= len(text) or text[i+1] not in '.([':
                            return i + 1
                    elif i >= 14 and text[i-14:i+1] == '.index.tolist()':
                        if i + 1 >= len(text) or text[i+1] not in '.([':
                            return i + 1
                    elif i >= 8 and text[i-8:i+1] == '.tolist()':
                        if i + 1 >= len(text) or text[i+1] not in '.([':
                            return i + 1

            i += 1

        return -1

    # Use regex to find all potential df/pd expression starts
    pattern = r'\b(df|pd)[\[\.\(]'

    result = []
    last_end = 0

    for match in re.finditer(pattern, spec_json):
        start = match.start()

        # Skip if this match is within an already-processed region
        if start < last_end:
            continue

        # Copy everything before this match
        result.append(spec_json[last_end:start])

        # Try to find the end of this expression
        expr_end = scan_for_tolist_end(spec_json, start)

        if expr_end != -1:
            expr = spec_json[start:expr_end]

            # Try to evaluate
            try:
                value = eval(expr, {"df": df, "pd": pd})
                # Successfully evaluated - replace with the value
                result.append(json.dumps(value))
                last_end = expr_end
                continue
            except Exception as e:
                # Evaluation failed - keep original
                pass

        # If we couldn't evaluate, just copy the match itself
        result.append(spec_json[start:match.end()])
        last_end = match.end()

    # Copy any remaining text
    result.append(spec_json[last_end:])

    return ''.join(result)


def render_plotly_chart(spec_json, df):
    """Render Plotly chart from JSON spec"""
    import plotly.graph_objects as go

    # Evaluate all Python expressions in the JSON
    processed_json = evaluate_python_expressions(spec_json, df)

    spec = json.loads(processed_json)
    fig = go.Figure(spec)
    st.plotly_chart(fig, use_container_width=True)


def render_echarts_chart(spec_json, df):
    """Render ECharts chart from JSON option"""
    from streamlit_echarts import st_echarts

    # Evaluate all Python expressions in the JSON
    processed_json = evaluate_python_expressions(spec_json, df)

    option = json.loads(processed_json)
    st_echarts(options=option, height="500px")
