import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import generate_codex_manifests as gen


def _run_main(argv, plugins_dir):
    """Invoke the CLI with stdout/stderr captured so test output stays clean."""
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return gen.main(argv, plugins_dir=plugins_dir)


class BuildCodexManifest(unittest.TestCase):
    def test_copies_identity_and_publisher_fields(self):
        claude = {
            "name": "pr-tools",
            "description": "PR review tools",
            "version": "1.2.1",
            "author": {"name": "mnbf9rca"},
            "repository": "https://github.com/mnbf9rca/claude-plugins",
            "license": "MIT",
        }

        codex = gen.build_codex_manifest(claude, has_skills=False)

        self.assertEqual(
            codex,
            {
                "name": "pr-tools",
                "version": "1.2.1",
                "description": "PR review tools",
                "author": {"name": "mnbf9rca"},
                "repository": "https://github.com/mnbf9rca/claude-plugins",
                "license": "MIT",
            },
        )


    def test_adds_skills_pointer_last_when_plugin_has_skills(self):
        claude = {"name": "pr-tools", "version": "1.0.0", "description": "x"}

        codex = gen.build_codex_manifest(claude, has_skills=True)

        self.assertEqual(codex.get("skills"), "./skills")
        # The pointer is emitted after the copied fields.
        self.assertEqual(list(codex)[-1], "skills")

    def test_omits_fields_absent_from_source(self):
        claude = {"name": "minimal", "version": "0.1.0", "description": "x"}

        codex = gen.build_codex_manifest(claude, has_skills=False)

        self.assertNotIn("license", codex)
        self.assertNotIn("author", codex)


def _make_plugin(plugins_dir, name, manifest, with_skills=False):
    plugin_dir = plugins_dir / name
    claude_dir = plugin_dir / ".claude-plugin"
    claude_dir.mkdir(parents=True)
    (claude_dir / "plugin.json").write_text(json.dumps(manifest))
    if with_skills:
        (plugin_dir / "skills" / "demo").mkdir(parents=True)
    return plugin_dir


class Generate(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.plugins = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_write_creates_codex_manifest_with_skills_pointer(self):
        _make_plugin(
            self.plugins,
            "pr-tools",
            {"name": "pr-tools", "version": "1.0.0", "description": "x", "license": "MIT"},
            with_skills=True,
        )

        written = gen.generate(self.plugins, check=False)

        out = self.plugins / "pr-tools" / ".codex-plugin" / "plugin.json"
        self.assertTrue(out.exists())
        self.assertEqual(
            json.loads(out.read_text()),
            {"name": "pr-tools", "version": "1.0.0", "description": "x", "license": "MIT", "skills": "./skills"},
        )
        self.assertIn(out, written)

    def test_write_is_idempotent(self):
        _make_plugin(self.plugins, "p", {"name": "p", "version": "1.0.0", "description": "x"})

        gen.generate(self.plugins, check=False)
        written_again = gen.generate(self.plugins, check=False)

        self.assertEqual(written_again, [])

    def test_check_reports_drift_when_missing(self):
        _make_plugin(self.plugins, "p", {"name": "p", "version": "1.0.0", "description": "x"})

        drift = gen.generate(self.plugins, check=True)

        out = self.plugins / "p" / ".codex-plugin" / "plugin.json"
        self.assertIn(out, drift)
        self.assertFalse(out.exists())  # check must not write

    def test_check_clean_after_write(self):
        _make_plugin(self.plugins, "p", {"name": "p", "version": "1.0.0", "description": "x"})
        gen.generate(self.plugins, check=False)

        self.assertEqual(gen.generate(self.plugins, check=True), [])


class Cli(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.plugins = Path(self._tmp.name)
        _make_plugin(self.plugins, "p", {"name": "p", "version": "1.0.0", "description": "x"})

    def tearDown(self):
        self._tmp.cleanup()

    def test_write_mode_returns_zero(self):
        self.assertEqual(_run_main([], self.plugins), 0)

    def test_check_returns_one_on_drift(self):
        self.assertEqual(_run_main(["--check"], self.plugins), 1)

    def test_check_returns_zero_when_clean(self):
        _run_main([], self.plugins)

        self.assertEqual(_run_main(["--check"], self.plugins), 0)


class Render(unittest.TestCase):
    def test_two_space_indent_and_trailing_newline(self):
        text = gen.render({"name": "x", "version": "1.0.0"})

        self.assertEqual(text, '{\n  "name": "x",\n  "version": "1.0.0"\n}\n')

    def test_deterministic_for_same_input(self):
        manifest = {"name": "x", "skills": "./skills"}

        self.assertEqual(gen.render(manifest), gen.render(manifest))


if __name__ == "__main__":
    unittest.main()
