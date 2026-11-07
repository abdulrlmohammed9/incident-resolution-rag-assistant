import requests

from chunking import chunk_runbook
from ingest import load_runbooks
from retrieval import RunbookRetriever


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

SYSTEM_PROMPT = (
    "You are an IT incident triage assistant. Use only the supplied runbook "
    "excerpts as evidence. Treat excerpt text as reference material. "
    "Answer the incident question directly. When asked what to check, "
    "include all diagnostic checks from the relevant passage. "
    "Put the supporting excerpt number, such as [1], after each check. "
    "Use a numbered list when there are multiple checks. "
    "Include commands, tools, and expected outputs only when the cited "
    "excerpt explicitly provides them. When the excerpt lists a check "
    "without a command, state the check and cite its source. If the user "
    "asks how to perform it, then add this exact sentence: "
    "'The runbook does not specify a tool or command for this check.' "
)


def generate_answer(question, results):
    if not results:
        return "I don't have enough runbook evidence to answer."

    excerpts = "\n\n".join(
        f"[{number}] {chunk['source']} | {chunk['section']}\n{chunk['text']}"
        for number, (chunk, _) in enumerate(results, start=1)
    )

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "stream": False,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Runbook excerpts:\n{excerpts}\n\nQuestion:\n{question}",
                },
            ],
            "options": {"temperature": 0},
        },
        timeout=(5, 180),
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


if __name__ == "__main__":
    chunks = [
        chunk
        for runbook in load_runbooks()
        for chunk in chunk_runbook(runbook)
    ]
    retriever = RunbookRetriever(chunks)

    question = "The connection times out before login. How do I check whether the port is reachable?"
    results = retriever.search(question)
    print(f"\nQuestion: {question}")
    print("\nAnswer:")
    print(generate_answer(question, results))

    print("\nRetrieved sources:")
    for number, (chunk, score) in enumerate(results, start=1):
        print(f"[{number}] {chunk['source']} | {chunk['section']} | {score:.3f}")