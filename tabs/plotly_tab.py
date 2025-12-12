import streamlit as st
from utils import (
    call_llm_api,
    extract_json_spec,
    get_dataset_info,
    get_plotly_prompt,
    render_plotly_chart
)


def render_plotly_tab(df, api_key_input, model_choice):
    """Render Plotly tab with chat interface"""
    st.subheader("💬 Chat with Your Data")

    # Display chat messages
    chat_container_plotly = st.container(height=300)
    with chat_container_plotly:
        for message in st.session_state.messages_plotly:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    with st.form(key="chat_form_plotly", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            prompt_plotly = st.text_input("", placeholder="Ask for a Plotly visualization...", label_visibility="collapsed", key="plotly_input")
        with col2:
            submit_plotly = st.form_submit_button("Send", use_container_width=True)

    if submit_plotly and prompt_plotly:
        if not api_key_input:
            st.error("Please enter your OpenRouter API key in the sidebar")
        else:
            st.session_state.messages_plotly.append({"role": "user", "content": prompt_plotly})

            dataset_info, numeric_cols, categorical_cols = get_dataset_info(df)

            try:
                system_prompt = get_plotly_prompt(dataset_info, df.columns.tolist(), numeric_cols, categorical_cols)

                messages = [
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages_plotly
                ]

                assistant_message = call_llm_api(api_key_input, model_choice, messages)
                st.session_state.messages_plotly.append({"role": "assistant", "content": assistant_message})

                spec_text = extract_json_spec(assistant_message)
                st.session_state.current_plotly_spec = spec_text
                st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.markdown("---")
    st.subheader("📈 Plotly Visualization")

    if st.session_state.current_plotly_spec:
        st.success("✅ Chart spec generated!")
        with st.expander("View Generated Plotly Spec"):
            st.code(st.session_state.current_plotly_spec, language="json")

        if st.button("Clear Plotly Chart"):
            st.session_state.current_plotly_spec = None
            st.rerun()

        try:
            render_plotly_chart(st.session_state.current_plotly_spec, df)
        except Exception as e:
            st.error(f"Error rendering chart: {e}")
            st.info("Try rephrasing your request or ask to fix the error.")
            # Show the problematic spec
            st.write("**Problematic spec:**")
            st.text(st.session_state.current_plotly_spec)
    else:
        st.info("💡 Ask me to create a Plotly visualization in the chat above.")
