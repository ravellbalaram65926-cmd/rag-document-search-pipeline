"""ETL demo: hash local documents and create overlapping retrieval chunks."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "raw" / "docs"
DEFAULT_OUTPUT = ROOT / "data" / "gold" / "chunks.jsonl"


def chunk_documents(input_dir: Path, chunk_words: int = 40, overlap: int = 8) -> list[dict[str, object]]:
    if chunk_words <= 0 or overlap < 0 or overlap >= chunk_words:
        raise ValueError("Require chunk_words > overlap >= 0")
    chunks = []
    seen_hashes = set()
    for path in sorted(input_dir.rglob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if digest in seen_hashes:
            continue
        seen_hashes.add(digest)
        words = text.split()
        step = chunk_words - overlap
        for start in range(0, len(words), step):
            part = words[start : start + chunk_words]
            if not part:
                continue
            chunks.append(
                {
                    "source": path.name,
                    "sha256": digest,
                    "start_word": start,
                    "text": " ".join(part),
                }
            )
    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--chunk-words", type=int, default=40)
    parser.add_argument("--overlap", type=int, default=8)
    args = parser.parse_args()
    chunks = chunk_documents(args.input_dir, args.chunk_words, args.overlap)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as target:
        for chunk in chunks:
            target.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    print(f"Indexed {len(chunks)} chunks from {args.input_dir}")


if __name__ == "__main__":
    main()
