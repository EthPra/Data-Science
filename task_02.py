import matplotlib.pyplot as plt
from utils import load_data


def make_plot() -> plt.Figure:

    df = load_data()

    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Autumn'

    df['season'] = df['month'].apply(get_season)
    
    df['time_hour'] = (df['period'] - 1) / 2.0
    
    seasons = ['Winter', 'Spring', 'Summer', 'Autumn']
    plot_cols = ['solar_mw', 'wind_mw', 'gas_mw', 'nuclear_mw']
    df_seasonal_avg = df.groupby(['season', 'time_hour'])[plot_cols].mean()
    

    colors = {
        'solar_mw': 'gold',
        'wind_mw': 'skyblue',
        'gas_mw': 'gray',
        'nuclear_mw': 'lightgreen'
    }
    
    labels = {
        'solar_mw': 'Solar',
        'wind_mw': 'Wind',
        'gas_mw': 'Gas',
        'nuclear_mw': 'Nuclear'
    }

    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10), sharex=True)
    fig.suptitle("Average Generation (MW) by Time of Day and Season (2024)", fontsize=16)

    
    max_y = df_seasonal_avg[plot_cols].max().max() * 1.05
    
    
    for ax, season in zip(axes.flat, seasons):
        if season in df_seasonal_avg.index:
            data_to_plot = df_seasonal_avg.loc[season]
            
            for col in plot_cols:
                ax.plot(
                    data_to_plot.index, 
                    data_to_plot[col], 
                    label=labels[col], 
                    color=colors[col],
                    linewidth=2
                )
            
            ax.set_title(season, fontsize=14)
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.set_ylim(0, max_y) 
            ax.set_ylabel("Average Generation (MW)")
            ax.set_xticks(range(0, 25, 3)) 
            ax.set_xlabel("Time of Day (Hour)")
        
    
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='center right', bbox_to_anchor=(1.05, 0.5), fontsize=14, title="Energy Source")
    
    
    plt.tight_layout()
    
    return fig
    

def get_caption() -> str:
    """Returns a short caption (a few sentences) that explains the figure."""

    return "Figure 2: A 2x2 grid of line plots showing the avg energy generation (MW) by time of day for each defined season in 2024"
    
def get_answer() -> str:
    """Return some text that answers the task question."""

    return (
        "Gas generation peaks during winter months at 17:30, reaching 14000 MW."
        "Gas generation peaks at 19:30 during summer, reaching approximately 8200 MW"
    )

   
if __name__ == "__main__":
    """Quick test of this task on its own."""

    PLOT_FILE = "report/figures/plot_02.png"
    print("Caption:\n", get_caption())
    print("\nAnswer:\n", get_answer())
    fig = make_plot()
    fig.savefig(PLOT_FILE, dpi=600, bbox_inches="tight")
    plt.show()
    plt.close(fig)
    print(f"\nPlot saved to {PLOT_FILE}")
