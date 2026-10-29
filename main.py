import os

from src.charts import save_charts
from src.insights import load_tickets, summarize
from src.report import write_report


def main():
    os.makedirs("output", exist_ok=True)
    tickets = load_tickets("data/tickets.csv")
    summary = summarize(tickets)
    save_charts(summary, "output")
    write_report(summary, "output/report.md")
    print(f"Analysed {summary['total']} tickets ({summary['sla_met_pct']}% met SLA). "
          "Report saved to output/report.md")


if __name__ == "__main__":
    main()