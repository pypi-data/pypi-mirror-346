import numpy as np
import pandas as pd

def result_stats(df: pd.DataFrame) -> dict:

    """
    Computes the number of home wins, draws, and away wins from the full-time result column ('FTR').

    Args:
        df (pd.DataFrame): DataFrame containing match data with a column 'FTR' indicating match outcomes.
            - 'H' for Home Win
            - 'D' for Draw
            - 'A' for Away Win

    Returns:
        dict: a dictionary with the counts of each result type, structured as:
            {
                'Home Wins': int,
                'Draws': int,
                'Away Wins': int
            }

    Raises:
        ValueError: if the 'FTR' column is not found in the DataFrame
    """
    if 'FTR' not in df.columns:
        raise ValueError("Column 'FTR' (full-time result) not found.")

    result_counts = df['FTR'].value_counts().to_dict()
    return{
        'Home Wins': result_counts.get('H', 0),
        'Draws': result_counts.get('D', 0),
        'Away Wins': result_counts.get('A', 0)
    }

def team_performance(df: pd.DataFrame, team_name: str) -> dict:

    """
    Computes a team's performance statistics across a season.

    This function summarizes key performance metrics for a specified team, including the number of matches played, wins, draws, losses, goals scored, goals conceded, goal difference, and points.

    Args:
        df (pd.DataFrame): dataFrame containing match data with columns 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR'.
        team_name (str): the name of the team for which the performance metrics will be calculated

    Returns:
        dict: a dictionary containing the team's performance metrics with the following structure:
            {
                'Team': str,
                'Matches': int,
                'Wins': int,
                'Draws': int,
                'Losses': int,
                'Goals For': int,
                'Goals Against': int,
                'Goal Difference': int,
                'Points': int
            }

    Raises:
        ValueError: if any of the required columns ('HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR') are missing
    """
    required_columns = ['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    matches = df[(df['HomeTeam'] == team_name) | (df['AwayTeam'] == team_name)]

    wins = draws = losses = goals_for = goals_against = 0

    for _, row in matches.iterrows():
        if row['HomeTeam'] == team_name:
            gf, ga = row['FTHG'], row['FTAG']
            result = row['FTR']
            if result == 'H': wins += 1
            elif result == 'D': draws += 1
            else: losses += 1
        else:  # Away team
            gf, ga = row['FTAG'], row['FTHG']
            result = row['FTR']
            if result == 'A': wins += 1
            elif result == 'D': draws += 1
            else: losses += 1

        goals_for += gf
        goals_against += ga

    return {
        'Team': team_name,
        'Matches': len(matches),
        'Wins': wins,
        'Draws': draws,
        'Losses': losses,
        'Goals For': goals_for,
        'Goals Against': goals_against,
        'Goal Difference': goals_for - goals_against,
        'Points': 3 * wins + draws
    }

def get_all_teams(df: pd.DataFrame) -> np.ndarray:
    
    """
    Extracts a list of all unique team names from 'HomeTeam' and 'AwayTeam' columns.

    This function aggregates unique team names from both the 'HomeTeam' and 'AwayTeam' columns to provide a comprehensive list of teams in the dataset.

    Args:
        df (pd.DataFrame): dataFrame containing match data with 'HomeTeam' and 'AwayTeam' columns

    Returns:
        np.ndarray: a sorted array of unique team names

    Raises:
        ValueError: if either 'HomeTeam' or 'AwayTeam' columns are missing
    """

    required_columns = ['HomeTeam', 'AwayTeam']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    
    home_teams = df['HomeTeam'].astype(str).unique()
    away_teams = df['AwayTeam'].astype(str).unique()
    all_teams = np.union1d(home_teams, away_teams)
    return all_teams

def each_team_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes performance statistics for every team in the dataset.

    This function calculates the performance metrics for each team using the `team_performance()` function and returns a DataFrame summarizing each team's performance.

    Args:
        df (pd.DataFrame): dataFrame containing match data with 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR' columns

    Returns:
        pd.DataFrame: a DataFrame where each row represents a team's performance summary, sorted by points in descending order
        Columns include:
            - 'Team': Team name
            - 'Matches': Matches played
            - 'Wins': Wins
            - 'Draws': Draws
            - 'Losses': Losses
            - 'Goals For': Goals scored
            - 'Goals Against': Goals conceded
            - 'Goal Difference': Goal difference
            - 'Points': Points accumulated
    """
    teams = get_all_teams(df)
    summaries = [team_performance(df, team) for team in teams]
    return pd.DataFrame(summaries).sort_values(by='Points', ascending=False).reset_index(drop=True)