import json
import os
import unittest

from worker import report


class FakeHttp:
    def __init__(self):
        self.calls = []

    def request(self, method, url, **kw):
        self.calls.append((method, url))

        class R:
            data = json.dumps([{"day": "2026-10-01"}, {"day": "2026-10-01"}]).encode()

        return R()


class ReportTest(unittest.TestCase):
    def test_build_report(self):
        out = report.build_report([{"day": "a"}, {"day": "a"}, {"day": "b"}])
        self.assertEqual(out, {"days": {"a": 2, "b": 1}, "total": 3})

    def test_run_reads_then_uploads(self):
        os.environ["REPORT_SOURCE_URL"] = "http://source.test/data"
        os.environ["REPORT_SINK_URL"] = "http://sink.test/out"
        http = FakeHttp()
        out = report.run(http)
        self.assertEqual(out["total"], 2)
        self.assertEqual([c[0] for c in http.calls], ["GET", "PUT"])


if __name__ == "__main__":
    unittest.main()
