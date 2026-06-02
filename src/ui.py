import streamlit as st
from pathlib import Path


def load_css(css_file_path: Path):
        """Inject custom CSS into the Streamlit app."""
        if css_file_path.exists():
                with open(css_file_path) as f:
                        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_header():
        """Simple header suitable for a lightweight UI."""
        st.markdown("<h1 style='text-align:center;margin:0'>PRISM</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:gray;margin-top:4px;margin-bottom:18px'>Convert documents to Markdown quickly.</p>", unsafe_allow_html=True)


def render_file_info(file_name: str, file_type: str, file_size: str, timestamp: str):
        """Render a minimal file info card."""
        st.markdown(
                f"""
                <div class="file-info-card">
                        <p><strong>File:</strong> {file_name}</p>
                        <p><strong>Type:</strong> {file_type} &nbsp; • &nbsp; <strong>Size:</strong> {file_size}</p>
                        <p style='color:gray;font-size:0.85rem'>Uploaded: {timestamp}</p>
                </div>
                """,
                unsafe_allow_html=True,
        )


def render_empty_state():
                """Render a minimal empty state prompting the user to upload a file."""
                st.markdown(
                                """
                                <div style='text-align:center;margin-top:24px;'>
                                        <p style='font-size:1.05rem;margin:0;color:#444;'>No document uploaded yet</p>
                                        <p style='color:gray;margin-top:6px;'>Upload a file to convert it to Markdown. Supported: PDF, DOCX, PPTX, XLSX, CSV, TXT, JPG, PNG.</p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                )
