import pandas as pd

from src.insights import categorize, prepare, summarize


def test_categorize_known_subjects():
    assert categorize("Backup failed after Windows update") == "Backup failure"
    assert categorize("Need to restore deleted folder") == "Restore request"
    assert categorize("Firewall blocking backup") == "Connectivity"


def test_categorize_unknown_subject():
    assert categorize("Printer is jammed") == "Other"


def test_sla_percentage():
    df = pd.DataFrame({
        "ticket_id": ["T1", "T2"],
        "created_at": pd.to_datetime(["2026-01-01", "2026-01-02"]),
        "subject": ["Cannot log in to account", "Upload very slow"],
        "priority": ["High", "Low"],
        "resolution_hours": [2, 100],  # first meets SLA, second misses
    })
    assert summarize(prepare(df))["sla_met_pct"] == 50.0