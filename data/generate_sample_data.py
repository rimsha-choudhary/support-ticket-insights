import csv
import random
from datetime import datetime, timedelta

ISSUES = {
    "Backup failure": ["Backup stalled at 0%", "Backup failed after Windows update",
                       "Backup not running overnight"],
    "Restore request": ["Need to restore deleted folder", "Full system restore after laptop crash",
                        "Restore files to new computer"],
    "Sign-in / account": ["Cannot log in to account", "Password reset not working",
                          "Two-factor code not received"],
    "Licensing": ["License expired warning", "Need to add another computer to plan",
                  "Renewal charge question"],
    "Connectivity": ["Backup stuck - no internet connection", "Upload very slow",
                     "Firewall blocking backup"],
}
SLA_HOURS = {"High": 4, "Medium": 24, "Low": 72}


def main(n=300, path="data/tickets.csv"):
    random.seed(42)  # same data every run
    start = datetime(2026, 1, 1)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ticket_id", "created_at", "customer_type", "subject",
                         "priority", "resolution_hours"])
        for i in range(1, n + 1):
            category = random.choice(list(ISSUES))
            subject = random.choice(ISSUES[category])
            priority = random.choices(list(SLA_HOURS), weights=[2, 5, 3])[0]
            created = start + timedelta(hours=random.randint(0, 24 * 180))
            hours = round(random.uniform(0.2, SLA_HOURS[priority] * 1.3), 1)
            writer.writerow([f"T{i:04d}", created.isoformat(timespec="minutes"),
                             random.choice(["Home", "SMB", "Enterprise"]),
                             subject, priority, hours])
    print(f"Wrote {n} tickets to {path}")


if __name__ == "__main__":
    main()