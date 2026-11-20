from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "patches"))
from apply_source_fixes import apply_fixes  # noqa: E402


class SourceOverlayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        (self.project / "tests").mkdir()
        self.test_file = self.project / "tests" / "run_tests.gd"
        self.test_file.write_text(
            '\tstate["run"] = {"stage": 3, "wave": 1, "started_at": 1000.0, "session": session}\n'
            '\tvar save_manager = GameStateScript.new()\n'
            '\t_expect(str(normalized["run"]["session"]["node_type"]) == "puzzle", "نوع العقدة المستعادة يجب أن يطابق المرحلة")\n',
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_replaces_wrong_stage_three_fixture_with_canonical_world_map_type(self):
        apply_fixes(self.project)
        result = self.test_file.read_text(encoding="utf-8")
        self.assertIn('state["run"]["session"]["node_type"] = "boss"', result)
        self.assertIn('== WorldMap.get_node_type(3)', result)
        self.assertNotIn('== "puzzle"', result)

    def test_patch_is_idempotent(self):
        apply_fixes(self.project)
        once = self.test_file.read_text(encoding="utf-8")
        apply_fixes(self.project)
        self.assertEqual(self.test_file.read_text(encoding="utf-8"), once)

    def test_unknown_source_shape_fails_closed(self):
        self.test_file.write_text("extends SceneTree\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            apply_fixes(self.project)


if __name__ == "__main__":
    unittest.main()
