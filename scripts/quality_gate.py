"""Quality Gate: gagalkan pipeline jika temuan Bandit melewati ambang batas."""
import json
import os
import sys

MAX_HIGH = int(os.environ.get("MAX_HIGH", "0"))
MAX_MEDIUM = int(os.environ.get("MAX_MEDIUM", "0"))


def main(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for r in data.get("results", []):
        counts[r["issue_severity"]] += 1
    print(f"Temuan -> HIGH={counts['HIGH']} MEDIUM={counts['MEDIUM']} LOW={counts['LOW']}")
    print(f"Ambang  -> MAX_HIGH={MAX_HIGH} MAX_MEDIUM={MAX_MEDIUM}")
    if counts["HIGH"] > MAX_HIGH or counts["MEDIUM"] > MAX_MEDIUM:
        print("QUALITY GATE: FAILED")
        return 1
    print("QUALITY GATE: PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
