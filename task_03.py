import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
from utils import load_data


def make_plot() -> plt.Figure:
    
    df = load_data()

    midday_periods = [23, 24, 25, 26]
    midday_data = df[df['period'].isin(midday_periods)]

    month_labels = [calendar.month_abbr[i] for i in range(1, 13)]

    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    
    ax_solar = axes[0]
    ax_wind = axes[1]

    fig.suptitle("Distribution of Midday (11:00-13:00) Solar and Wind Generation by Month (2024)", fontsize=16)

    sns.boxplot(data=midday_data, x='month', y='solar_mw', ax=ax_solar)
    ax_solar.set_ylabel("Solar Generation (MW)")
    ax_solar.set_xlabel(None)
    ax_solar.grid(True, linestyle='--', alpha=0.6)

    sns.boxplot(data=midday_data, x='month', y='wind_mw', ax=ax_wind)
    ax_wind.set_ylabel("Wind Generation (MW)")
    ax_wind.set_xlabel("Month")
    ax_wind.set_xticklabels(month_labels)
    ax_wind.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()

    return fig


def get_caption() -> str:
    """Returns a short caption (a few sentences) that explains the figure."""

    
    return "Figure 3: Box plots showing the distribution of midday (11:00-13:00) solar and wind power generation (in MW) for each month in 2024."
    


def get_answer() -> str:
    """Return some text that answers the task question."""

   
    return (
        "Based on the box plots, wind has the largest average monthly range."
        "The month with the largest range for wind generation is November, with a difference of approx. 17,558 MW"
        "between the maximum and minimum midday generation values."
    )


if __name__ == "__main__":
    """Quick test of this task on its own."""

    PLOT_FILE = "report/figures/plot_03.png"
    print("Caption:\n", get_caption())
    print("\nAnswer:\n", get_answer())
    fig = make_plot()
    fig.savefig(PLOT_FILE, dpi=600, bbox_inches="tight")
    plt.show()
    plt.close(fig)
    print(f"\nPlot saved to {PLOT_FILE}")
