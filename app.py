import os
import time
from datetime import datetime
import streamlit as st
from pathlib import Path

from src.config import APP_NAME, ASSETS_DIR, UPLOAD_DIR, OUTPUT_DIR, SUPPORTED_EXTENSIONS, MAX_FILE_SIZE_MB
from src.utils import (
    format_file_size, get_safe_filename, generate_default_output_name,
    count_text_stats, cleanup_file
)
from src.converter import convert_to_markdown
from src.ui import (
    load_css, render_header, render_file_info, render_empty_state
)

# --- Page Config ---
st.set_page_config(
    page_title=APP_NAME,
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load custom CSS (asset file is `style.css`)
load_css(ASSETS_DIR / "style.css")

# --- Session State Initialization ---
if 'conversion_done' not in st.session_state:
    st.session_state.conversion_done = False
if 'markdown_content' not in st.session_state:
    st.session_state.markdown_content = ""
if 'stats' not in st.session_state:
    st.session_state.stats = {}
if 'uploaded_filepath' not in st.session_state:
    st.session_state.uploaded_filepath = ""

def clear_session():
    """Reset the app state."""
    if st.session_state.uploaded_filepath:
        cleanup_file(st.session_state.uploaded_filepath)
    st.session_state.conversion_done = False
    st.session_state.markdown_content = ""
    st.session_state.stats = {}
    st.session_state.uploaded_filepath = ""

# --- Header ---
render_header()

# --- Main App Logic (simple layout) ---
uploaded_file = st.file_uploader(
    "Drag & drop your file here or click to browse",
    type=[ext.replace('.', '') for ext in SUPPORTED_EXTENSIONS],
    help="Supported formats: PDF, DOCX, PPTX, XLSX, CSV, TXT, JPG, PNG"
)

default_out_name = ""
if uploaded_file is not None:
    file_ext = Path(uploaded_file.name).suffix.lower()
    if file_ext not in SUPPORTED_EXTENSIONS:
        st.error(f"Unsupported file format: {file_ext}")
        uploaded_file = None
    else:
        max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
        if hasattr(uploaded_file, "size") and uploaded_file.size > max_bytes:
            st.error(f"File exceeds maximum allowed size of {MAX_FILE_SIZE_MB} MB.")
            uploaded_file = None

if uploaded_file is not None:
    default_out_name = generate_default_output_name(uploaded_file.name)

custom_filename = st.text_input("Output filename (without .md)", value=default_out_name)

if uploaded_file is not None and st.button("Convert to Markdown"):
    # proceed with conversion
    safe_upload_name = get_safe_filename(uploaded_file.name)
    upload_path = UPLOAD_DIR / safe_upload_name
    with open(upload_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.session_state.uploaded_filepath = str(upload_path)

    try:
        with st.spinner("Converting document via MarkItDown..."):
            start_time = time.time()
            md_text = convert_to_markdown(str(upload_path))
            duration = time.time() - start_time

            chars, words = count_text_stats(md_text)

            st.session_state.markdown_content = md_text
            st.session_state.stats = {
                "chars": chars,
                "words": words,
                "time": f"{duration:.2f}s",
                "filename": get_safe_filename(custom_filename or default_out_name) + ".md"
            }
            st.session_state.conversion_done = True
            st.rerun()
    except Exception as e:
        st.error(f"An error occurred: {e}")
        cleanup_file(str(upload_path))

# --- Main App Logic ---
if not st.session_state.conversion_done:
    # Show empty state or file preview
    if uploaded_file is None:
        render_empty_state()
    else:
        # Display uploaded file info and allow conversion
        file_size_str = format_file_size(uploaded_file.size)
        upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        render_file_info(uploaded_file.name, file_ext.upper(), file_size_str, upload_time)

        st.markdown("---")

        # Show preview of small text files
        try:
            if Path(uploaded_file.name).suffix.lower() in {".txt", ".csv"}:
                uploaded_file.seek(0)
                content_preview = uploaded_file.getvalue().decode("utf-8", errors="ignore")[:2000]
                st.text_area("Preview (first 2k chars)", value=content_preview, height=200)
        except Exception:
            pass

        if convert_btn:
            # The conversion is handled by the top-level Convert button.
            # This branch was leftover and referenced an undefined `convert_btn`.
            pass

else:
        # --- Results View ---
        st.success("Conversion completed successfully!")

        col1, col2, col3 = st.columns(3)
        col1.metric("Word Count", st.session_state.stats['words'])
        col2.metric("Character Count", st.session_state.stats['chars'])
        col3.metric("Conversion Time", st.session_state.stats['time'])

        tab1, tab2 = st.tabs(["Markdown Source", "Rendered Preview"])

        with tab1:
            st.code(st.session_state.markdown_content, language="markdown")

        with tab2:
            st.markdown(st.session_state.markdown_content)

        st.markdown("---")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button(
                label="Download Markdown",
                data=st.session_state.markdown_content,
                file_name=st.session_state.stats['filename'],
                mime="text/markdown",
                type="primary",
                use_container_width=True
            )
        with c2:
            if st.button("Copy to Clipboard", use_container_width=True):
                st.toast("Feature limited by browser security in plain Streamlit. Please copy manually from the Source tab.")
        with c3:
            if st.button("Convert Another File", use_container_width=True):
                clear_session()
                st.rerun()

        if st.button("Clear Session & Delete Temp Files", use_container_width=True):
            clear_session()
            st.rerun()