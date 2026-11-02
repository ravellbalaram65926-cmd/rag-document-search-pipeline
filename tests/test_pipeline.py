import tempfile
import unittest
from pathlib import Path

from src.main import chunk_documents


class DocumentPipelineTests(unittest.TestCase):
    def test_chunks_have_stable_source_hash_and_overlap(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.txt"
            path.write_text("one two three four five six", encoding="utf-8")
            chunks = chunk_documents(Path(directory), chunk_words=4, overlap=1)
        self.assertEqual(chunks[0]["text"], "one two three four")
        self.assertEqual(chunks[1]["text"], "four five six")
        self.assertEqual(chunks[0]["sha256"], chunks[1]["sha256"])


if __name__ == "__main__":
    unittest.main()
