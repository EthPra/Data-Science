import pandas as pd
import matplotlib.pyplot as plt
import calendar
from utils import load_data


def make_plot() -> plt.Figure:
    
    df = load_data()
    
    df_monthly_avg = df.groupby('month')[['solar', 'wind', 'gas', 'nuclear', 'imports', 'other']].mean()
    
    labels = ['solar', 'wind', 'gas', 'nuclear', 'imports', 'other']
    
    colors = {
        'solar': 'gold',
        'wind': 'skyblue',
        'gas': 'gray',
        'nuclear': 'lightgreen',
        'imports': 'purple',
        'other': 'saddlebrown'
    }
    month_names = {i: calendar.month_name[i] for i in range(1, 13)}

    fig, axes = plt.subplots(3, 4, figsize=(16, 12))
    fig.suptitle("Monthly Average Energy Mix (2024)", fontsize=16)

    for month in range(1, 13):
        ax = axes.flat[month-1]
        
        if month in df_monthly_avg.index:
            data = df_monthly_avg.loc[month]
            ax.pie(
                data,
                labels=None,
                colors=[colors[label] for label in data.index],
                autopct='%1.1f%%',
                startangle=90,
                pctdistance=0.85
            )
            ax.set_title(month_names[month])
        else:
            ax.set_title(month_names[month])
            ax.text(0.5, 0.5, "No Data", horizontalalignment='center', verticalalignment='center')

    legend_handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    
    fig.legend(
        legend_handles,
        labels,
        loc='center right',
        bbox_to_anchor=(1.05, 0.5),
        fontsize=14,
        title="Energy Sources"
    )
    
    plt.tight_layout() 
    
    return fig

def get_caption() -> str:
    """Returns a short caption (a few sentences) that explains the figure."""
    
    return "This figure presents a 3x4 grid of pie charts, each representing the monthly average energy mix for 2024."
    
def get_answer() -> str:
    """Return some text that answers the task question."""

    return (
        " November had the biggest percentage contribution of Gas energy at 38%. "
        "December had the lowest solar energy at 0.8%."
    )
    

if __name__ == "__main__":
    """Quick test of this task on its own."""

    PLOT_FILE = "report/figures/plot_01.png"
    print("Caption:\n", get_caption())
    print("\nAnswer:\n", get_answer())
    fig = make_plot()
    fig.savefig(PLOT_FILE, dpi=600, bbox_inches="tight")
    plt.show()
    plt.close(fig)
    print(f"\nPlot saved to {PLOT_FILE}")
