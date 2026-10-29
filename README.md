# Support Ticket Insights

Support teams collect a lot of ticket data but rarely turn it into decisions.
This tool reads a CSV of support tickets and produces a short, client-ready
report: which issues drive the most volume, where SLA targets are missed,
and what to fix first.

I built it from my experience supporting a cloud backup platform at OpenText.
All data in this repo is fictional.

## What it does
- Sorts tickets into issue types from their subject lines
- Measures SLA performance and average resolution time by issue type
- Charts ticket volume by type and by month
- Writes an executive summary with an LLM (Google Gemini), with a
  rule-based fallback when no API key is set

## Sample output
![Tickets by issue type](output/tickets_by_category.png)

See the full report: [output/report.md](output/report.md)

## How to run
    pip install -r requirements.txt
    python data/generate_sample_data.py
    python main.py
    python -m pytest

Optional: set a GEMINI_API_KEY environment variable for the AI summary.

## Tools
Python, pandas, matplotlib, pytest, Google Gemini API.
Built with help from ChatGPT and Claude for prototyping and debugging.

## What I'd add next
- Upload a CSV through a simple web page
- Track repeat customers and escalation rates