import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from check_docs import check_file, check_repo, markdown_links


class DocumentationLinksTest(unittest.TestCase):
    def test_ignores_fenced_code_and_external_links(self):
        sample = '[Open](https://github.com)\n```md\n[missing](bad.md)\n```\n[Local](ok.md)'
        self.assertEqual(list(markdown_links(sample)), [(1, "https://github.com"), (5, "ok.md")])

    def test_valid_relative_target_and_fragment(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "target.md").write_text("# Title\n", encoding="utf-8")
            readme = root / "README.md"
            readme.write_text("[Target](target.md#title) [Same](#local)\n", encoding="utf-8")
            self.assertEqual(check_repo(root), [])

    def test_missing_target_detected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            readme = root / "README.md"
            readme.write_text("[Missing](absent.md)\n", encoding="utf-8")
            self.assertIn("missing local file", check_file(readme, root)[0])

    def test_parent_escape_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "repo"
            root.mkdir()
            readme = root / "README.md"
            readme.write_text("[Escape](../outside.md)\n", encoding="utf-8")
            self.assertIn("escapes repository", check_file(readme, root)[0])

    def test_encoded_filename(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "file name.md").write_text("test", encoding="utf-8")
            readme = root / "README.md"
            readme.write_text("[Encoded](file%20name.md)\n", encoding="utf-8")
            self.assertEqual(check_file(readme, root), [])

    def test_absolute_path_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            readme = root / "README.md"
            readme.write_text("[System](/etc/passwd)\n", encoding="utf-8")
            self.assertIn("invalid local link", check_file(readme, root)[0])

    def test_ignored_generated_directories(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("# Main\n", encoding="utf-8")
            out = root / "node_modules"
            out.mkdir()
            (out / "README.md").write_text("[Broken](fake.md)\n", encoding="utf-8")
            self.assertEqual(check_repo(root), [])


if __name__ == "__main__":
    unittest.main()
