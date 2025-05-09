from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("pyTSPA_toolbox")
except PackageNotFoundError:
    __version__ = "0.0.2"

from .data import load_match_data, clean_data, data_profiling
from .metrics import result_stats, team_performance, get_all_teams, each_team_performance

__all__ = [
    "load_match_data",
    "clean_data",
    "data_profiling",
    "result_stats",
    "team_performance",
    "get_all_teams",
    "each_team_performance",
    "__version__",
]