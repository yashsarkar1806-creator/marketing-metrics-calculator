import json, pathlib, subprocess, sys, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import metrics as m

ROOT = pathlib.Path(__file__).resolve().parents[1]

class TestMetrics(unittest.TestCase):
    def test_basics(self):
        self.assertEqual(m.cac(1000, 20), 50)
        self.assertAlmostEqual(m.roas(3000, 1000), 3.0)
        self.assertAlmostEqual(m.break_even_roas(0.5), 2.0)
        self.assertIsNone(m.cac(1000, 0))
        self.assertAlmostEqual(m.ltv_saas(100, 0.8, 0.02), 4000)
        self.assertAlmostEqual(m.ltv_dtc(50, 2, 3, 0.6), 180)

    def test_dtc_report(self):
        r = m.report("dtc", json.load(open(ROOT / "examples/dtc_skincare.json")))
        self.assertAlmostEqual(r["cac"], 50)
        self.assertAlmostEqual(r["ltv"], 210.8)
        self.assertAlmostEqual(r["ltv_to_cac"], 4.216)
        self.assertAlmostEqual(r["roas"], 2.8)

    def test_saas_report(self):
        r = m.report("saas", json.load(open(ROOT / "examples/saas_startup.json")))
        self.assertAlmostEqual(r["cac"], 500)
        self.assertAlmostEqual(r["ltv"], 3840)
        self.assertAlmostEqual(r["payback_months"], 500 / 96)

    def test_cli(self):
        out = subprocess.run([sys.executable, str(ROOT / "metrics.py"), "saas", "--file",
                              str(ROOT / "examples/saas_startup.json")], capture_output=True, text=True, check=True).stdout
        self.assertIn("LTV:CAC", out)

if __name__ == "__main__":
    unittest.main()
