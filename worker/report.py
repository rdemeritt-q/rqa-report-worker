import json
import os

import urllib3


def build_report(rows):
    """Count events per day from rows like {"day": "2026-10-01"}."""
    counts = {}
    for row in rows:
        counts[row["day"]] = counts.get(row["day"], 0) + 1
    return {"days": counts, "total": sum(counts.values())}


def run(http=None):
    http = http or urllib3.PoolManager()
    source = http.request("GET", os.environ["REPORT_SOURCE_URL"], timeout=10)
    report = build_report(json.loads(source.data))
    http.request(
        "PUT",
        os.environ["REPORT_SINK_URL"],
        body=json.dumps(report).encode(),
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    return report


if __name__ == "__main__":
    run()
