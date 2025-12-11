import requests
import json


def call_llm_api(api_key, model, messages):
    """Call OpenRouter API and return assistant message"""
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": messages
        }
    )
    response.raise_for_status()
    response_data = response.json()
    return response_data["choices"][0]["message"]["content"]


def extract_json_spec(text):
    """Extract JSON from LLM response"""
    spec_text = text.strip()
    if "```" in spec_text:
        spec_text = spec_text.split("```json")[-1].split("```")[0].strip()
        if not spec_text:
            spec_text = text.split("```")[-2].strip()
    return spec_text


def extract_vegalite_spec(assistant_message):
    """Extract Vega-Lite spec from LLM response"""
    if "{" in assistant_message and "}" in assistant_message:
        start_idx = assistant_message.find("{")
        brace_count = 0
        end_idx = start_idx
        for i in range(start_idx, len(assistant_message)):
            if assistant_message[i] == "{":
                brace_count += 1
            elif assistant_message[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i + 1
                    break

        spec_str = assistant_message[start_idx:end_idx]
        spec_data = json.loads(spec_str)

        if "$schema" in spec_data or "mark" in spec_data:
            return spec_data
    return None


def get_dataset_info(df):
    """Get dataset context for LLM"""
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    return f"""
Dataset Information:
Total Records: {len(df)}
Columns: {', '.join(df.columns)}

Numeric columns: {', '.join(numeric_cols)}
Categorical columns: {', '.join(categorical_cols)}

Sample data (first 3 rows):
{df.head(3).to_string()}

Data types:
{df.dtypes.to_string()}
""", numeric_cols, categorical_cols
