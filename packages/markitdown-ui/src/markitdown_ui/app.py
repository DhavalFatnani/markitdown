# SPDX-FileCopyrightText: 2024-present Adam Fourney <adamfo@microsoft.com>
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import io
import os
from typing import Optional

import streamlit as st
from markitdown import MarkItDown, MarkItDownException, StreamInfo

from markitdown_ui.__about__ import __version__


@st.cache_resource
def get_converter() -> MarkItDown:
    return MarkItDown()


def _output_filename(source_name: str) -> str:
    base, _ = os.path.splitext(source_name)
    return f"{base or 'document'}.md"


def _convert_upload(uploaded_file) -> tuple[str, str]:
    stream = io.BytesIO(uploaded_file.getvalue())
    stream_info = StreamInfo(
        filename=uploaded_file.name,
        extension=os.path.splitext(uploaded_file.name)[1],
        mimetype=uploaded_file.type,
    )
    result = get_converter().convert_stream(stream, stream_info=stream_info)
    return result.markdown, _output_filename(uploaded_file.name)


def _convert_url(url: str) -> tuple[str, str]:
    result = get_converter().convert(url.strip())
    title = result.title or "document"
    safe_title = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in title)
    return result.markdown, f"{safe_title or 'document'}.md"


def run() -> None:
    st.set_page_config(
        page_title="MarkItDown",
        page_icon="📄",
        layout="wide",
    )

    st.title("MarkItDown")
    st.caption(
        "Convert documents to Markdown for LLMs and text pipelines. "
        f"v{__version__}"
    )

    file_tab, url_tab = st.tabs(["Upload file", "From URL"])

    source_name: Optional[str] = None
    markdown: Optional[str] = None
    error: Optional[str] = None

    with file_tab:
        uploaded = st.file_uploader(
            "Choose a file",
            type=None,
            help="PDF, Word, PowerPoint, Excel, HTML, images, audio, and more.",
        )
        if uploaded is not None:
            with st.spinner("Converting..."):
                try:
                    markdown, source_name = _convert_upload(uploaded)
                except MarkItDownException as exc:
                    error = str(exc)
                except Exception as exc:
                    error = f"Conversion failed: {exc}"

    with url_tab:
        url = st.text_input(
            "Page URL",
            placeholder="https://example.com/page or https://www.youtube.com/watch?v=...",
        )
        convert_url = st.button("Convert URL", type="primary", disabled=not url.strip())
        if convert_url and url.strip():
            with st.spinner("Fetching and converting..."):
                try:
                    markdown, source_name = _convert_url(url)
                except MarkItDownException as exc:
                    error = str(exc)
                except Exception as exc:
                    error = f"Conversion failed: {exc}"

    if error:
        st.error(error)

    if markdown is not None and source_name is not None:
        st.success(f"Converted **{source_name}**")

        preview_tab, raw_tab = st.tabs(["Preview", "Raw Markdown"])
        with preview_tab:
            st.markdown(markdown)
        with raw_tab:
            st.text_area(
                "Markdown output",
                value=markdown,
                height=480,
                label_visibility="collapsed",
            )

        st.download_button(
            label="Download .md",
            data=markdown,
            file_name=source_name,
            mime="text/markdown",
            type="primary",
        )


run()
