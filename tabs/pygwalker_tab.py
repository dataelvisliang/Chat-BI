import streamlit as st
import pygwalker as pyg
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit.components.v1 as components
from utils import (
    call_llm_api,
    extract_vegalite_spec,
    get_dataset_info,
    get_vegalite_prompt
)


def render_pygwalker_tab(df, api_key_input, model_choice):
    """Render PygWalker tab with chat interface"""
    st.subheader("💬 Chat with Your Data")

    # Display chat messages
    chat_container = st.container(height=300)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            prompt = st.text_input("", placeholder="Ask me about the data or request a visualization...", label_visibility="collapsed")
        with col2:
            submit = st.form_submit_button("Send", use_container_width=True)

    if submit and prompt:
        if not api_key_input:
            st.error("Please enter your OpenRouter API key in the sidebar")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})

            dataset_info, numeric_cols, categorical_cols = get_dataset_info(df)

            try:
                system_prompt = get_vegalite_prompt(dataset_info, numeric_cols, categorical_cols)

                messages = [
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages
                ]

                assistant_message = call_llm_api(api_key_input, model_choice, messages)
                st.session_state.messages.append({"role": "assistant", "content": assistant_message})

                # Try to extract Vega-Lite spec
                spec_data = extract_vegalite_spec(assistant_message)
                if spec_data:
                    st.session_state.current_spec = spec_data
                    st.session_state.spec_version += 1

                st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")

    st.markdown("---")

    # Visualization section
    st.subheader("📊 Interactive Visualization")

    if st.session_state.current_spec:
        st.success("✅ Chart generated from AI! You can modify it below or ask for a different visualization.")
        with st.expander("View Generated Vega-Lite Spec"):
            st.json(st.session_state.current_spec)

        if st.button("Clear AI Chart"):
            st.session_state.current_spec = None
            st.session_state.spec_version += 1
            st.rerun()

    # Render with PygWalker
    try:
        if st.session_state.current_spec:
            renderer = StreamlitRenderer(
                df,
                spec=st.session_state.current_spec,
                key=f"pygwalker_{st.session_state.spec_version}"
            )
            renderer.explorer()
        else:
            st.info("💡 Ask me to create a visualization in the chat above, or drag fields manually below.")
            renderer = StreamlitRenderer(
                df,
                key=f"pygwalker_default_{st.session_state.spec_version}"
            )
            renderer.explorer()
    except Exception as e:
        st.error(f"Error rendering chart: {e}")
        st.write("Falling back to default interface...")
        pyg_html = pyg.to_html(df)
        components.html(pyg_html, height=700, scrolling=True)
