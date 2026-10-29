import os


def rule_based_summary(summary):
    cat = summary["by_category"]
    top = cat.index[0]
    worst = cat["sla_met_pct"].idxmin()
    return (
        f"{summary['total']} tickets were analysed and {summary['sla_met_pct']}% met SLA. "
        f"'{top}' drives the most volume ({cat.loc[top, 'tickets']} tickets). "
        f"'{worst}' has the weakest SLA result ({cat.loc[worst, 'sla_met_pct']}%), "
        f"so it is the first place to improve."
    )


def ai_summary(summary):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    from google import genai

    client = genai.Client(api_key=api_key)
    prompt = (
        "You are advising the head of a customer support team. In under 150 words, "
        "explain these results in plain business language, then give 3 specific "
        "recommendations.\n\n"
        f"Total tickets: {summary['total']}\n"
        f"SLA met overall: {summary['sla_met_pct']}%\n"
        f"{summary['by_category'].to_string()}"
    )
    try:
        response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
        return response.text
    except Exception as error:
        print(f"AI summary failed ({error}); using rule-based summary.")
        return None


def write_report(summary, path):
    text = ai_summary(summary) or rule_based_summary(summary)
    lines = [
        "# Support Ticket Insights Report", "",
        "## Executive summary", "", text, "",
        "## Results by issue type", "",
        summary["by_category"].to_markdown(), "",
        "![Tickets by issue type](tickets_by_category.png)", "",
        "![Tickets per month](tickets_per_month.png)", "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))