import matplotlib
matplotlib.use("Agg")  # save images without opening a window
import matplotlib.pyplot as plt

BLUE = "#0f62fe"


def save_charts(summary, out_dir):
    fig, ax = plt.subplots(figsize=(8, 4))
    summary["by_category"]["tickets"].plot.barh(ax=ax, color=BLUE)
    ax.invert_yaxis()
    ax.set_title("Tickets by issue type")
    ax.set_xlabel("Tickets")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(f"{out_dir}/tickets_by_category.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    summary["monthly"].plot(ax=ax, marker="o", color=BLUE)
    ax.set_title("Tickets per month")
    ax.set_xlabel("")
    ax.set_ylabel("Tickets")
    fig.tight_layout()
    fig.savefig(f"{out_dir}/tickets_per_month.png")
    plt.close(fig)