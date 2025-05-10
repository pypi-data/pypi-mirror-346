import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler

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

def win_percentage(df: pd.DataFrame, team_name: str) -> float:
    
    """
    Calculates the win percentage for a specified team.

    Args:
        df (pd.DataFrame): DataFrame containing match data with 'HomeTeam', 'AwayTeam', and 'FTR' columns
        team_name (str): the name of the team to calculate win percentage for

    Returns:
        float: the win percentage as a value between 0 and 1

    Raises:
        ValueError: if the required columns are missing
    """
    required_columns = ['HomeTeam', 'AwayTeam', 'FTR']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Missing required columns: {required_columns}")

    matches = df[(df['HomeTeam'] == team_name) | (df['AwayTeam'] == team_name)]
    total_matches = len(matches)
    if total_matches == 0:
        return 0.0

    wins = sum((matches['HomeTeam'] == team_name) & (matches['FTR'] == 'H')) + sum((matches['AwayTeam'] == team_name) & (matches['FTR'] == 'A'))
    return (wins / total_matches)

def each_win_percentage(df: pd.DataFrame) -> pd.DataFrame:

    """
    Calculates the win percentage for every team and returns it as a separate DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing match data with 'HomeTeam', 'AwayTeam', and 'FTR' columns

    Returns:
        pd.DataFrame: DataFrame with 'Team' and 'WinPercentage' columns
    """
    teams = pd.concat([df['HomeTeam'], df['AwayTeam']]).unique()
    win_percentages = {team: win_percentage(df, team) for team in teams}

    result_df = pd.DataFrame(list(win_percentages.items()), columns=['Team', 'WinPercentage'])
    return result_df

def pythagorean_expectation(df: pd.DataFrame, team_name: str, exponent: float = 2.0) -> float:

    """
    Calculates the Pythagorean Expectation for a specified team using match data.

    Args:
        df (pd.DataFrame): DataFrame containing match data with 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG' columns
        team_name (str): the name of the team to calculate the Pythagorean Expectation for
        exponent (float): exponent value for the calculation, default is 2.0

    Returns:
        float: the Pythagorean Expectation as a value between 0 and 1
    
    Raises:
        ValueError: if the required columns are missing
    """
    required_columns = ['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Missing required columns: {required_columns}")

    matches = df[(df['HomeTeam'] == team_name) | (df['AwayTeam'] == team_name)]

    goals_for = sum(matches[matches['HomeTeam'] == team_name]['FTHG']) + sum(matches[matches['AwayTeam'] == team_name]['FTAG'])
    goals_against = sum(matches[matches['HomeTeam'] == team_name]['FTAG']) + sum(matches[matches['AwayTeam'] == team_name]['FTHG'])

    if goals_for + goals_against == 0:
        return 0.0

    gf_exp = goals_for ** exponent
    ga_exp = goals_against ** exponent
    return gf_exp / (gf_exp + ga_exp)

def each_pythagorean_expectation(df: pd.DataFrame, exponent: float = 2.0) -> pd.DataFrame:

    """
    Calculates the Pythagorean Expectation for every team and returns it as a separate DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing match data with 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG' columns
        exponent (float): exponent value for the calculation, default is 2.0

    Returns:
        pd.DataFrame: DataFrame with 'Team' and 'PythagoreanExpectation' columns
    """
    teams = pd.concat([df['HomeTeam'], df['AwayTeam']]).unique()
    pyth_expectations = {team: pythagorean_expectation(df, team, exponent) for team in teams}

    result_df = pd.DataFrame(list(pyth_expectations.items()), columns=['Team', 'PythagoreanExpectation'])
    return result_df

def logistic_regression_prediction(df: pd.DataFrame) -> dict:
    """
    Predicts match outcomes (Win/Draw/Loss) using multinomial logistic regression with oversampling and additional features.

    Args:
        df (pd.DataFrame): DataFrame containing match data with necessary metrics calculated

    Returns:
        dict: a dictionary containing model accuracy, confusion matrix, predictions, and the trained model
    """
    wpc = each_win_percentage(df)
    pyth = each_pythagorean_expectation(df)

    team_stats = pd.merge(wpc, pyth, on="Team", how="left")
    df = df.merge(team_stats, left_on="HomeTeam", right_on="Team", how="left").rename(
        columns={
            "WinPercentage": "Home_WinPercentage",
            "PythagoreanExpectation": "Home_PythagoreanExpectation"
        }
    )
    df = df.merge(team_stats, left_on="AwayTeam", right_on="Team", how="left").rename(
        columns={
            "WinPercentage": "Away_WinPercentage",
            "PythagoreanExpectation": "Away_PythagoreanExpectation"
        }
    )

    df['GoalDifference'] = df['Home_PythagoreanExpectation'] - df['Away_PythagoreanExpectation']

    # Target variable: 2 for Home Win, 1 for Draw, 0 for Away Win
    df["Target"] = df["FTR"].map({"H": 2, "D": 1, "A": 0})

    # Features and target
    X = df[[
        "Home_WinPercentage", 
        "Away_WinPercentage", 
        "Home_PythagoreanExpectation", 
        "Away_PythagoreanExpectation",
        "GoalDifference"
    ]]
    y = df["Target"].astype(int)

    # Standardize the features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Apply SMOTE for oversampling the minority classes
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.3, random_state=42)

    # Multinomial Logistic Regression model with regularization
    model = LogisticRegression(solver='lbfgs', max_iter=1000, C=1.0)
    model.fit(X_train, y_train)

    # Predictions and evaluation
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    conf_matrix = confusion_matrix(y_test, predictions, labels=[2, 1, 0])

    # Create a DataFrame with predictions and actual results
    prediction_df = pd.DataFrame(X_test, columns=[
        "Home_WinPercentage", "Away_WinPercentage", "Home_PythagoreanExpectation", "Away_PythagoreanExpectation", "GoalDifference"
    ])
    prediction_df["Actual"] = y_test.values
    prediction_df["Predicted"] = predictions

    return {
        "accuracy": accuracy,
        "confusion_matrix": conf_matrix.tolist(),
        "predictions": prediction_df.reset_index(drop=True),
        "model": model
    }

def predict_match_outcome(home_team: str, away_team: str, model: LogisticRegression, df: pd.DataFrame) -> dict:

    """
    Predicts the outcome of a specific match between two teams using the trained logistic regression model.

    Args:
        home_team (str): name of the home team
        away_team (str): name of the away team
        model (LogisticRegression): trained logistic regression model
        df (pd.DataFrame): DataFrame containing the match data

    Returns:
        dict: a dictionary containing predicted outcome and probabilities
    """
    wpc = each_win_percentage(df)
    pyth = each_pythagorean_expectation(df)
    team_stats = pd.merge(wpc, pyth, on="Team", how="left")

    home_stats = team_stats[team_stats["Team"] == home_team]
    away_stats = team_stats[team_stats["Team"] == away_team]

    if home_stats.empty or away_stats.empty:
        raise ValueError("One or both teams not found in the dataset!")

    X_new = pd.DataFrame({
        "Home_WinPercentage": [home_stats["WinPercentage"].values[0]],
        "Away_WinPercentage": [away_stats["WinPercentage"].values[0]],
        "Home_PythagoreanExpectation": [home_stats["PythagoreanExpectation"].values[0]],
        "Away_PythagoreanExpectation": [away_stats["PythagoreanExpectation"].values[0]],
        "GoalDifference": [home_stats["PythagoreanExpectation"].values[0] - away_stats["PythagoreanExpectation"].values[0]]
    })

    probabilities = model.predict_proba(X_new)[0]
    prediction = model.predict(X_new)[0]

    outcome_map = {2: "Home Win", 1: "Draw", 0: "Away Win"}
    predicted_outcome = outcome_map[prediction]

    return {
        "predicted_outcome": predicted_outcome,
        "probabilities": {
            "Home Win": round(probabilities[2], 3),
            "Draw": round(probabilities[1], 3),
            "Away Win": round(probabilities[0], 3)
        }
    }

def season_half_prediction(df: pd.DataFrame) -> pd.DataFrame:

    """
    Predicts the outcomes of the second half of the season based on the Pythagorean Expectation values calculated from the first half of the season.

    Args:
        df (pd.DataFrame): DataFrame containing match data with 'Date', 'HomeTeam', 'AwayTeam' and 'FTR' columns

    Returns:
        pd.DataFrame: DataFrame with predicted outcomes for the second half of the season
    """
    df = df.sort_values(by="Date")
    mid_index = len(df) // 2
    first_half = df.iloc[:mid_index]
    second_half = df.iloc[mid_index:]

    # Calculate Pythagorean Expectation for the first half
    pyth_expectations = each_pythagorean_expectation(first_half)

    # Merge with second half data
    second_half = second_half.merge(pyth_expectations, left_on="HomeTeam", right_on="Team", how="left").rename(
        columns={"PythagoreanExpectation": "Home_PythagoreanExpectation"}
    )
    second_half = second_half.merge(pyth_expectations, left_on="AwayTeam", right_on="Team", how="left").rename(
        columns={"PythagoreanExpectation": "Away_PythagoreanExpectation"}
    )

    # Calculate predicted outcome based on Pythagorean Expectation
    second_half["PredictedOutcome"] = np.where(
        second_half["Home_PythagoreanExpectation"] > second_half["Away_PythagoreanExpectation"], "Home Win",
        np.where(
            second_half["Home_PythagoreanExpectation"] < second_half["Away_PythagoreanExpectation"], "Away Win",
            "Draw"
        )
    )

    return second_half[["Date", "HomeTeam", "AwayTeam", "FTR", "Home_PythagoreanExpectation", "Away_PythagoreanExpectation", "PredictedOutcome"]]