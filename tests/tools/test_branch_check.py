"""Tests for tools/branch_check.py.

test_reports_unpushed_and_lagging_integration_branch: local main ahead of and behind its upstream
    is reported both ways.
test_reports_landed_branch_after_cherry_pick: a branch whose change reached the upstream under a
    different hash is reported as landed, not unlanded.
test_reports_unowned_unlanded_branch: an unlanded branch without a description is reported; a
    described one is not.
test_reports_clean_landed_worktree: a clean worktree whose head is on the upstream is removable.
test_post_tool_use_runs_only_after_push: the PostToolUse hook reports after a git push command only.
test_no_integration_values_no_report: a repository without Integration values gets no report.
"""

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

TOOL = Path(__file__).resolve().parents[2] / "tools" / "branch_check.py"
SPEC = importlib.util.spec_from_file_location("branch_check", TOOL)
branch_check = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(branch_check)

VALUES = "## Integration\n- integration.branch: main\n- integration.upstream: origin/main\n- integration.branch_lifetime: 1 day\n"


def run(directory, *args):
    subprocess.run(["git", "-C", str(directory), *args], check=True, capture_output=True)


def commit(directory, name):
    (directory / name).write_text(name, encoding="utf-8")
    run(directory, "add", name)
    run(directory, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--no-verify", "-m", name)


class BranchCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.remote, self.repo = root / "remote.git", root / "repo"
        subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(self.remote)], check=True)
        subprocess.run(["git", "clone", "-q", str(self.remote), str(self.repo)], check=True, capture_output=True)
        run(self.repo, "config", "core.hooksPath", "/dev/null")
        rules = self.repo / ".claude" / "rules" / "project"
        rules.mkdir(parents=True)
        (rules / "integration.md").write_text(VALUES, encoding="utf-8")
        commit(self.repo, "base")
        run(self.repo, "push", "-q", "origin", "main")

    def tearDown(self):
        self.tmp.cleanup()

    def findings(self):
        return "\n".join(branch_check.report(self.repo, fetch=True))

    def test_reports_unpushed_and_lagging_integration_branch(self):
        commit(self.repo, "local")
        self.assertIn("1 commit(s) not on origin/main", self.findings())
        run(self.repo, "switch", "-q", "-C", "main", "origin/main")
        other = Path(self.tmp.name) / "other"
        subprocess.run(["git", "clone", "-q", str(self.remote), str(other)], check=True, capture_output=True)
        commit(other, "remote")
        run(other, "push", "-q", "origin", "main")
        self.assertIn("lags origin/main by 1", self.findings())

    def test_reports_landed_branch_after_cherry_pick(self):
        run(self.repo, "switch", "-q", "-c", "wt/a")
        commit(self.repo, "a")
        run(self.repo, "switch", "-q", "main")
        run(self.repo, "-c", "user.name=u", "-c", "user.email=u@u", "cherry-pick", "wt/a")
        run(self.repo, "push", "-q", "origin", "main")
        text = self.findings()
        self.assertIn("every change on origin/main", text)
        self.assertNotIn("no branch description", text)

    def test_reports_unowned_unlanded_branch(self):
        run(self.repo, "switch", "-q", "-c", "wt/b")
        commit(self.repo, "b")
        run(self.repo, "switch", "-q", "-c", "wt/c")
        commit(self.repo, "c")
        run(self.repo, "config", "branch.wt/c.description", "T1 goal")
        run(self.repo, "switch", "-q", "main")
        text = self.findings()
        self.assertIn("no branch description (no owning row): wt/b", text)
        self.assertNotIn("wt/c", text.split("no owning row")[1])

    def test_reports_clean_landed_worktree(self):
        tree = Path(self.tmp.name) / "tree"
        run(self.repo, "worktree", "add", "-q", "--detach", str(tree), "origin/main")
        self.assertIn(f"remove them: {tree.resolve()}", self.findings())

    def test_post_tool_use_runs_only_after_push(self):
        commit(self.repo, "local")
        for command, expected in (("git status", ""), (f"git -C {self.repo} push origin main", "")):
            payload = '{"cwd": "%s", "tool_input": {"command": "%s"}}' % (self.repo, command)
            result = subprocess.run(
                ["python3", str(TOOL), "--hook", "PostToolUse", "--no-fetch"],
                input=payload, capture_output=True, text=True, check=True,
            )
            if command == "git status":
                self.assertEqual(result.stdout, expected)
            else:
                self.assertIn("not on origin/main", result.stdout)

    def test_no_integration_values_no_report(self):
        (self.repo / ".claude" / "rules" / "project" / "integration.md").unlink()
        commit(self.repo, "local")
        self.assertEqual(branch_check.report(self.repo, fetch=False), [])


if __name__ == "__main__":
    unittest.main()
