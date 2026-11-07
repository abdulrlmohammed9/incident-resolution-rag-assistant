from pathlib import Path

RUNBOOK_DIR = Path(__file__).resolve().parents[1] / "runbooks"


def load_runbooks():
    return [
        {"source": path.name, "text": path.read_text(encoding="utf-8")}
        for path in sorted(RUNBOOK_DIR.glob("*.md"))
    ]


if __name__ == "__main__":
    runbooks = load_runbooks()
    print(f"Loaded {len(runbooks)} runbook(s)")

    for runbook in runbooks:
        print(runbook["source"])
        print(runbook["text"].splitlines()[0])