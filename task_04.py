import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
from utils import load_data


def make_plot() -> plt.Figure:

    df = load_data()

    midday_periods = [23, 24, 25, 26]
    df_midday = df[df['period'].isin(midday_periods)].copy()
    
    
    months_to_plot = [5, 6, 7, 8] 
    df_filtered = df_midday[df_midday['month'].isin(months_to_plot)]

    fig, axes = plt.subplots(
        nrows=2, 
        ncols=2, 
        figsize=(12, 10)
    )
    
    month_names = {
        5: "May", 
        6: "June", 
        7: "July", 
        8: "August"
    }

    for ax, month_num in zip(axes.flat, months_to_plot):
        
        month_data = df_filtered[df_filtered['month'] == month_num]
        
        sns.regplot(
            data=month_data,
            x='solar_mw',
            y='wind_mw',
            ax=ax,
            scatter_kws={'alpha': 0.5, 's': 20}, 
            line_kws={'color': 'blue'},
            ci=None # disabled shading for clarity
        )
        
        ax.set_title(month_names[month_num], fontsize=16)
        ax.set_xlabel("Solar Generation (MW)")
        ax.set_ylabel("Wind Generation (MW)")
        ax.grid(True, linestyle='--', alpha=0.6)

    fig.suptitle("Relationship Between Midday Solar and Wind Generation (2024)", fontsize=16)
    
    plt.tight_layout()

    return fig


def get_caption() -> str:
    """Returns a short caption (a few sentences) that explains the figure."""
    
    return "Figure 4: A 2x2 grid of scatter plots showing the relationship between midday solar and wind power generation (in MW) for the months of May, June, July, and August in 2024. Each plot includes a trend line indicating the correlation between the two energy sources."


def get_answer() -> str:
    """Return some text that answers the task question."""
    return (
        "Based on the scatter plots, theres a clear negative correlation."
        "The plots and the trend lines all slope downwards, evoking that as solar generation increases wind generation tends to decrease."
        "Based on the analysis of the data, the highest observed wind generation when solar was above 6000 MW is approx 10600 MW"
    )


if __name__ == "__main__":
    """Quick test of this task on its own."""

    PLOT_FILE = "report/figures/plot_04.png"
    print("Caption:\n", get_caption())
    print("\nAnswer:\n", get_answer())
    
    fig = make_plot() 
    
    fig.savefig(PLOT_FILE, dpi=600, bbox_inches="tight")
    plt.show()
    plt.close(fig)
    print(f"\nPlot saved to {PLOT_FILE}")
