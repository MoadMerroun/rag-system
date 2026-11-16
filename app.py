import json
import os

import requests
import streamlit as st


DEFAULT_API_URL = os.getenv("RAG_API_URL", "http://127.0.0.1:8000")


def normalize_base_url(url: str) -> str:
    return url.strip().rstrip("/")


def upload_document(api_url: str, uploaded_file) -> tuple[bool, str]:
    try:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/octet-stream",
            )
        }
        response = requests.post(f"{api_url}/documents", files=files, timeout=120)
        response.raise_for_status()
        payload = response.json()

        return True, f"Uploaded {payload['filename']}: {payload['chunks']} chunks indexed."
    except requests.RequestException as exc:
        return False, f"Upload failed: {exc}"
    except json.JSONDecodeError:
        return False, "Upload failed: API returned a non-JSON response."


def format_answer(payload: dict) -> str:
    answer = payload["answer"]
    sources = payload.get("sources", [])
    if not sources:
        return answer

    lines = []
    for source in sources:
        page = source.get("page")
        # PyPDF pages are 0-based; show them 1-based to the user.
        label = source["filename"] if page is None else f"{source['filename']} (page {page + 1})"
        if label not in lines:
            lines.append(label)
    return answer + "\n\n**Sources:**\n" + "\n".join(f"- {line}" for line in lines)


def ask_question(api_url: str, question: str) -> tuple[bool, str]:
    try:
        response = requests.post(
            f"{api_url}/ask",
            json={"question": question},
            timeout=120,
        )
        response.raise_for_status()
        return True, format_answer(response.json())
    except requests.RequestException as exc:
        return False, f"Request failed: {exc}"
    except json.JSONDecodeError:
        return False, "Request failed: API returned a non-JSON response."


def main() -> None:
    st.set_page_config(page_title="RAG Client", page_icon=":books:", layout="wide")
    st.title("RAG API Client")

    with st.sidebar:
        st.subheader("Connection")
        api_url = st.text_input("Base API URL", value=DEFAULT_API_URL)
        api_url = normalize_base_url(api_url)
        st.caption("Example: http://127.0.0.1:8000")

    st.subheader("1. Upload document")
    uploaded_file = st.file_uploader("Choose a file", type=None)
    if st.button("Upload to /documents", disabled=uploaded_file is None):
        ok, message = upload_document(api_url, uploaded_file)
        if ok:
            st.success(message)
        else:
            st.error(message)

    st.subheader("2. Ask a question")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    question = st.chat_input("Ask something about uploaded documents")
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        ok, answer = ask_question(api_url, question)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.button("Clear chat"):
        st.session_state.chat_history = []
        st.rerun()


if __name__ == "__main__":
    main()
