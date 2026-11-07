import re

from ingest import load_runbooks


def chunk_runbook(runbook):
    # Each level-two heading starts a new passage.
    parts = re.split(r"^##[ \t]+", runbook["text"], flags=re.MULTILINE)

    # The text before the first section contains the title and system.
    header = parts[0].strip()
    chunks = []

    for part in parts[1:]:
        heading, _, body = part.partition("\n")
        section = heading.strip()
        body = body.strip()

        if section and body:
            chunks.append({
                "source": runbook["source"],
                "section": section,
                "text": f"{header}\n\n{section}\n{body}",
            })

    return chunks


if __name__ == "__main__":
    chunks = [
        chunk
        for runbook in load_runbooks()
        for chunk in chunk_runbook(runbook)
    ]

    print(f"Created {len(chunks)} passage(s)")
    for chunk in chunks:
        print(f"{chunk['source']} | {chunk['section']}")