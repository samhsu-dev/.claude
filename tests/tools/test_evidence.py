"""Tests for tools/evidence.py.

test_merge_lone_surrogate_value_round_trips: a run row whose value holds an undecodable source
    byte (a lone surrogate after JSON decoding) survives merge into the merged file unchanged.
test_merge_lone_surrogate_value_renders_escaped: the same row renders into EVIDENCE.md with the
    surrogate written as its backslash escape.
"""

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

TOOL = Path(__file__).resolve().parents[2] / "tools" / "evidence.py"
SPEC = importlib.util.spec_from_file_location("evidence", TOOL)
evidence = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evidence)

VALUE = "latin-1 byte \udce9 in source"


def merged_task(directory):
    task = Path(directory)
    run = task / "run-1"
    run.mkdir()
    row = {"kind": "corpus", "claim": "One case is not UTF-8.", "source": "count cases", "value": VALUE}
    (run / evidence.RUN_FILE).write_text(json.dumps(row) + "\n")
    with redirect_stdout(io.StringIO()):
        evidence.merge(task, task)
    return task


class MergeSurrogateTest(unittest.TestCase):
    def test_merge_lone_surrogate_value_round_trips(self):
        with tempfile.TemporaryDirectory() as directory:
            task = merged_task(directory)
            self.assertEqual([r["value"] for r in evidence.load(task / evidence.MERGED)], [VALUE])

    def test_merge_lone_surrogate_value_renders_escaped(self):
        with tempfile.TemporaryDirectory() as directory:
            task = merged_task(directory)
            self.assertIn("latin-1 byte \\udce9 in source", (task / evidence.RENDERED).read_text())


if __name__ == "__main__":
    unittest.main()
