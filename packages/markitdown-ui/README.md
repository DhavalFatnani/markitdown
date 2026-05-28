# MarkItDown UI

A lightweight browser UI for [MarkItDown](https://github.com/microsoft/markitdown).

## Installation

```bash
pip install markitdown-ui
```

Or from this repository:

```bash
pip install -e packages/markitdown-ui
```

## Usage

Start the local web app (use one of these — the bare commands may not be on your PATH):

```bash
python3 -m markitdown_ui
```

```bash
python3 -m streamlit run packages/markitdown-ui/src/markitdown_ui/app.py
```

If your Python scripts directory is on PATH, you can also use:

```bash
markitdown-ui
```

Streamlit opens at `http://localhost:8501` by default.

## Features

- Drag-and-drop file upload
- URL conversion (web pages, YouTube, etc.)
- Markdown preview and raw output
- Download converted `.md` files

## Security

This app runs locally with your user's file and network access, the same as the MarkItDown CLI. Do not expose it to untrusted networks without additional authentication.
