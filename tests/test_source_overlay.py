from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "patches"))
from apply_source_fixes import apply_fixes  # noqa: E402

OLD_STATUS = "أضيفت اختبارات GDScript تغطي هيكل الحملة، فتح المراحل، ألوان الندرات، مجموع احتمالات الندرة والضمانات، إعادة ضبط عدادات الحظ، أمثلة الكومبو، أولوية درع النواة، استمرارية سلامة النواة، صلاحية نقطة استعادة المعركة، رفض الجلسات المهزومة، ترحيل مخطط الحفظ القديم، تنظيف نقطة الاستعادة بعد الفوز/الخسارة، تحذير الزعيم، فتح الجذور، خسارة لا تفقد الموارد، والدمج الحتمي وشروطه. لم يمكن تشغيلها في بيئة الإنشاء الحالية لغياب Godot executable. فحص Python الساكن يتحقق من العقود المكتوبة داخل الملفات فقط ولا يعادل التحليل أو التشغيل داخل المحرك."
NEW_STATUS = "أضيفت اختبارات GDScript تغطي هيكل الحملة، فتح المراحل، ألوان الندرات، مجموع احتمالات الندرة والضمانات، إعادة ضبط عدادات الحظ، أمثلة الكومبو، أولوية درع النواة، استمرارية سلامة النواة، صلاحية نقطة استعادة المعركة، رفض الجلسات المهزومة، ترحيل مخطط الحفظ القديم، تنظيف نقطة الاستعادة بعد الفوز/الخسارة، تحذير الزعيم، فتح الجذور، خسارة لا تفقد الموارد، والدمج الحتمي وشروطه. اجتاز المشروع في GitHub Actions على Commit af6190ea94e4eb5ae74f906e30c235651df8e512 استيراد Godot 4.7.0 وتحليل السكربتات، ثم اجتازت اختبارات GDScript الـ16. كما نجحت اختبارات طبقة التصحيح الأربع وفحوصات Python الساكنة الـ113. هذا لا يثبت تصدير Android أو الأداء على جهاز فعلي؛ يلزم اختبار APK على أجهزة مستهدفة قبل الإصدار."


class SourceOverlayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        (self.project / "tests").mkdir()
        (self.project / "docs").mkdir()
        self.test_file = self.project / "tests" / "run_tests.gd"
        self.test_file.write_text(
            '\tstate["run"] = {"stage": 3, "wave": 1, "started_at": 1000.0, "session": session}\n'
            '\tvar save_manager = GameStateScript.new()\n'
            '\t_expect(str(normalized["run"]["session"]["node_type"]) == "puzzle", "نوع العقدة المستعادة يجب أن يطابق المرحلة")\n',
            encoding="utf-8",
        )
        self.status_file = self.project / "docs" / "IMPLEMENTATION_STATUS_AR.md"
        self.status_file.write_text(OLD_STATUS, encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_replaces_wrong_stage_three_fixture_with_canonical_world_map_type(self):
        apply_fixes(self.project)
        result = self.test_file.read_text(encoding="utf-8")
        self.assertIn('state["run"]["session"]["node_type"] = "boss"', result)
        self.assertIn('== WorldMap.get_node_type(3)', result)
        self.assertNotIn('== "puzzle"', result)

    def test_updates_implementation_status_to_match_verified_ci(self):
        apply_fixes(self.project)
        result = self.status_file.read_text(encoding="utf-8")
        self.assertIn("af6190ea94e4eb5ae74f906e30c235651df8e512", result)
        self.assertIn("اختبارات GDScript الـ16", result)
        self.assertNotIn("لم يمكن تشغيلها", result)

    def test_patch_is_idempotent(self):
        apply_fixes(self.project)
        once_test = self.test_file.read_text(encoding="utf-8")
        once_status = self.status_file.read_text(encoding="utf-8")
        apply_fixes(self.project)
        self.assertEqual(self.test_file.read_text(encoding="utf-8"), once_test)
        self.assertEqual(self.status_file.read_text(encoding="utf-8"), once_status)

    def test_unknown_source_shape_fails_closed(self):
        self.test_file.write_text("extends SceneTree\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            apply_fixes(self.project)


if __name__ == "__main__":
    unittest.main()
