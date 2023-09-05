import requests
import pandas as pd
import numpy as np
import xgboost as xgb

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'bf3944d441mshfab1db9287934d6p168260jsn5fbb5574d0ea'
BASE_URL = 'https://api-football-v1.p.rapidapi.com/v3/fixtures'

# Define headers for the API request, including your API key
headers = {
    'X-RapidAPI-Key': API_KEY,
}

# Function to fetch fixtures for a specific league and season
def get_fixtures(league_id, season):
    # Specify the endpoint for fixtures data
    endpoint = f'fixtures?league={league_id}&season={season}'
    
    # Make a GET request to the API
    response = requests.get(BASE_URL + endpoint, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Extract and return the list of fixtures
        fixtures = data['response']
        return fixtures
    else:
        # Handle errors
        return None

# Function to make predictions
def predict_match_outcome(home_team, away_team, home_team_goals, away_team_goals):
    # Create a DataFrame with the input features
    input_data = pd.DataFrame({
        'home_team_goals': [home_team_goals],
        'away_team_goals': [away_team_goals]
        # Add more features as needed for your model
    })
    
    # Load your trained XGBoost model
    model = xgb.XGBClassifier(n_estimators=500, max_depth=5, learning_rate=0.1, random_state=42)
    
    # Make predictions using your trained model
    prediction = model.predict(input_data)[0]
    
    # Interpret the prediction (e.g., 1 for home team win, 0 for draw, -1 for away team win)
    if prediction == 1:
        outcome = "Home Team Win"
    elif prediction == 0:
        outcome = "Draw"
    else:
        outcome = "Away Team Win"
    
    return outcome

# Main function
def main():
    print("Welcome to the Sports Prediction Project!")
    
    # Example usage:
    league_id = [524,  775, 754, 891]  # Replace with the ID of your desired league
    season = '2023'  # Replace with the desired season
    #home_team = 'Manchester United'  # Replace with the desired home team
    #away_team = 'Liverpool'          # Replace with the desired away team
    
    # Fetch fixtures for the specified league and season
    fixtures = get_fixtures(league_id, season)
    
    if fixtures:
        # Find the fixture for the specified teams
        fixture = None
        for f in fixtures:
            if f['teams']['home'] == home_team and f['teams']['away'] == away_team:
                fixture = f
                break
        
        if fixture:
            # Extract relevant information from the fixture
            home_goals = fixture['goals']['home']
            away_goals = fixture['goals']['away']
            
            # Make a prediction for the match
            prediction = predict_match_outcome(home_team, away_team, home_goals, away_goals)
            print(f"Prediction for {home_team} vs. {away_team}: {prediction}")
        else:
            print(f"Fixture not found for {home_team} vs. {away_team}.")
    else:
        print("Failed to fetch fixtures.")

if __name__ == "__main__":
    main()
