import requests
import streamlit as st

from chunking import chunk_runbook
from generation import generate_answer
from ingest import load_runbooks
from retrieval import RunbookRetriever


st.set_page_config(page_title="Incident Navigator")
st.title("Incident Navigator")
st.caption("SFTP troubleshooting with runbook citations")


@st.cache_resource
def build_retriever():
    chunks = [
        chunk
        for runbook in load_runbooks()
        for chunk in chunk_runbook(runbook)
    ]
    return RunbookRetriever(chunks)


def show_sources(results):
    if results:
        with st.expander("Retrieved runbook passages"):
            for number, (chunk, score) in enumerate(results, start=1):
                st.text(
                    f"[{number}] {chunk['source']} | "
                    f"{chunk['section']} | Similarity {score:.3f}"
                )
                st.text(chunk["text"])


if "history" not in st.session_state:
    st.session_state.history = []

if st.sidebar.button("Clear chat"):
    st.session_state.history = []

for turn in st.session_state.history:
    with st.chat_message("user"):
        st.text(turn["question"])
    with st.chat_message("assistant"):
        st.markdown(turn["answer"])
        show_sources(turn["results"])

question = st.chat_input("Describe your SFTP incident")

if question and question.strip():
    question = question.strip()

    with st.chat_message("user"):
        st.text(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Checking the runbooks…"):
                results = build_retriever().search(question, top_k=4)
                answer = generate_answer(question, results)
        except requests.RequestException as error:
            st.error(f"Ollama request failed. Check that Ollama is running. {error}")
        else:
            st.markdown(answer)
            show_sources(results)
            st.session_state.history.append(
                {"question": question, "answer": answer, "results": results}
            )