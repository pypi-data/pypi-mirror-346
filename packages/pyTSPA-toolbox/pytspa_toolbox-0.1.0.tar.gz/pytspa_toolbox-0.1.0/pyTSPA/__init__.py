from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("pyTSPA_toolbox")
except PackageNotFoundError:
    __version__ = "0.0.3"

from .data import load_match_data, clean_data, data_profiling
from .metrics import result_stats, team_performance, get_all_teams, each_team_performance, win_percentage, each_win_percentage, pythagorean_expectation, each_pythagorean_expectation, logistic_regression_prediction, predict_match_outcome, season_half_prediction
from .visualization import plot_result_distribution, plot_team_results, plot_league_points_table, plot_goal_difference_distribution, plot_win_percentage_comparison, plot_pythagorean_expectation

__all__ = [
    "load_match_data",
    "clean_data",
    "data_profiling",
    "result_stats",
    "team_performance",
    "get_all_teams",
    "each_team_performance",
    "win_percentage",
    "each_win_percentage",
    "pythagorean_expectation",
    "each_pythagorean_expectation",
    "logistic_regression_prediction",
    "predict_match_outcome",
    "season_half_prediction",
    "plot_result_distribution",
    "plot_team_results",
    "plot_league_points_table",
    "plot_goal_difference_distribution",
    "plot_win_percentage_comparison",
    "plot_pythagorean_expectation",
    "__version__",
]