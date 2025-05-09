import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from pyTSPA.metrics import result_stats, team_performance

def plotting(wdl_stats, team_summary):
    """
    Plots:
    1. A Seaborn pie chart of league-wide Win/Draw/Loss stats
    2. A Seaborn bar chart of a team's Wins, Draws, Losses, and Goals
    """
    # Apply Seaborn theme
    sns.set_theme(style="whitegrid")

    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # --- Pie Chart using Seaborn-compatible approach ---
    wdl_df = pd.DataFrame(list(wdl_stats.items()), columns=['Result', 'Count'])
    axs[0].pie(
        wdl_df['Count'],
        labels=wdl_df['Result'],
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("pastel")
    )
    axs[0].set_title('League Results Distribution', fontsize=14)

    # --- Bar Chart using Seaborn ---
    performance_data = {
        'Metric': ['Wins', 'Draws', 'Losses', 'Goals For', 'Goals Against'],
        'Value': [
            team_summary['Wins'],
            team_summary['Draws'],
            team_summary['Losses'],
            team_summary['Goals For'],
            team_summary['Goals Against']
        ]
    }
    perf_df = pd.DataFrame(performance_data)

    sns.barplot(data=perf_df, x='Metric', y='Value', ax=axs[1], palette="deep")
    axs[1].set_title(f"{team_summary['Team']} Season Summary", fontsize=14)
    axs[1].bar_label(axs[1].containers[0], label_type='edge')

    plt.tight_layout()
    plt.show()

#from this point the plotting is implementeed
import seaborn as sns
import matplotlib.pyplot as plt

def plot_result_distribution(df):
    """
    Visualizes overall result distribution: Home Wins, Draws, Away Wins.
    """
    results = result_stats(df)
    result_names = list(results.keys())
    result_counts = list(results.values())

    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.barplot(x=result_names, y=result_counts, palette="muted")
    plt.title("Match Result Distribution")
    plt.ylabel("Number of Matches")
    plt.xlabel("Result")
    plt.tight_layout()
    plt.show()


def plot_team_results(df, team_name):
    """
    Plots wins, draws, and losses for a single team.
    """
    stats = team_performance(df, team_name)
    results = {
        'Wins': stats['Wins'],
        'Draws': stats['Draws'],
        'Losses': stats['Losses']
    }

    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 5))
    sns.barplot(x=list(results.keys()), y=list(results.values()), palette="deep")
    plt.title(f"{team_name} - Match Outcomes")
    plt.ylabel("Number of Matches")
    plt.xlabel("Result Type")
    plt.tight_layout()
    plt.show()

def plot_league_points_table(df):
    """
    Plots total points for all teams as a horizontal bar chart.
    Assumes df is the output of `each_team_performance()`.
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 12))
    sorted_df = df.sort_values(by="Points", ascending=True)

    sns.barplot(x="Points", y="Team", data=sorted_df, palette="viridis")
    plt.title("League Table - Points by Team")
    plt.xlabel("Points")
    plt.ylabel("Team")
    plt.tight_layout()
    plt.show()