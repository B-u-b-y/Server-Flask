import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from flask import send_file

def player_statistics(db):
    # Access the 'games' collection
    games_collection = db['appearances']
    games_data = list(games_collection.find())

    # Convert the data to a DataFrame
    df = pd.DataFrame(games_data)

    if df.empty:
        return None

    # Summing goals, assists, minutes played, yellow cards, and red cards for each player
    performance = df.groupby('player_name').agg(
        total_goals=('goals', 'sum'),
        total_assists=('assists', 'sum'),
        total_minutes=('minutes_played', 'sum'),
        yellow_cards=('yellow_cards', 'sum'),
        red_cards=('red_cards', 'sum')
    ).reset_index()

    performance['total_minutes'] = performance['total_minutes'] / 60  # Convert minutes to hours

    # Get the top 10 players by total goals
    top_performers = performance.sort_values(by='total_goals', ascending=False).head(15)

    # Set the positions and width for the bars
    bar_width = 0.10
    positions = np.arange(len(top_performers['player_name']))

    # Set the figure size
    plt.figure(figsize=(16, 8))  # Adjust the width and height as needed

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(14, 10))

    # Plot for Total Goals
    ax.bar(positions, top_performers['total_goals'], width=bar_width, label='Total Goals', color='skyblue')

    # Plot for Total Assists
    ax.bar(positions + bar_width, top_performers['total_assists'], width=bar_width, label='Total Assists', color='lightgreen')

    # Plot for Total Minutes Played
    ax.bar(positions + 2 * bar_width, top_performers['total_minutes'], width=bar_width, label='Total Hours Played', color='salmon')

    # Plot for Yellow Cards
    ax.bar(positions + 3 * bar_width, top_performers['yellow_cards'], width=bar_width, label='Total Yellow Cards', color='purple')

    # Plot for Red Cards
    ax.bar(positions + 4 * bar_width, top_performers['red_cards'], width=bar_width, label='Total Red Cards', color='green')

    # Set the x-axis ticks and labels
    ax.set_xticks(positions + bar_width)
    ax.set_xticklabels(top_performers['player_name'], rotation=90, ha='right')

    # Add titles and labels
    ax.set_title('Top 15 Players by Goals, Assists, and Minutes Played')
    ax.set_xlabel('Player Name')
    ax.set_ylabel('Count')
    ax.legend()
    ax.set_axisbelow(True)
    plt.grid(True, color = 'gray', linestyle = '--', linewidth = 0.5)

    # Adjust layout for better spacing
    plt.tight_layout()

    # Save plot to BytesIO
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')
