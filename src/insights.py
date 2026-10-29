import pandas as pd

SLA_HOURS = {"High": 4, "Medium": 24, "Low": 72}

CATEGORY_KEYWORDS = {
    "Backup failure": ["backup stalled", "backup failed", "not running"],
    "Restore request": ["restore"],
    "Sign-in / account": ["log in", "password", "two-factor"],
    "Licensing": ["license", "plan", "renewal"],
    "Connectivity": ["internet", "slow", "firewall"],
}


def categorize(subject):
    """Return the issue category for a ticket subject."""
    text = subject.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(word in text for word in keywords):
            return category
    return "Other"


def prepare(df):
    """Add category, SLA target and met_sla columns."""
    df = df.copy()
    df["category"] = df["subject"].apply(categorize)
    df["sla_hours"] = df["priority"].map(SLA_HOURS)
    df["met_sla"] = df["resolution_hours"] <= df["sla_hours"]
    return df


def load_tickets(path):
    df = pd.read_csv(path, parse_dates=["created_at"])
    return prepare(df)


def summarize(df):
    by_category = (
        df.groupby("category")
        .agg(tickets=("ticket_id", "count"),
             avg_hours=("resolution_hours", "mean"),
             sla_met_pct=("met_sla", "mean"))
        .sort_values("tickets", ascending=False)
    )
    by_category["avg_hours"] = by_category["avg_hours"].round(1)
    by_category["sla_met_pct"] = (by_category["sla_met_pct"] * 100).round(1)

    monthly = df.set_index("created_at").resample("ME")["ticket_id"].count()

    return {
        "total": len(df),
        "sla_met_pct": round(df["met_sla"].mean() * 100, 1),
        "by_category": by_category,
        "monthly": monthly,
    }