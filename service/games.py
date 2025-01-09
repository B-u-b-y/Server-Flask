import matplotlib
matplotlib.use('Agg') #used for non-interactive backend

import base64
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from io import BytesIO
from flask import jsonify, send_file
import geopandas as gpd

def test_method(db):
    # Access the 'games' collection
    games_collection = db['games']
    games_data = list(games_collection.find())

    # Convert the data to a DataFrame
    df = pd.DataFrame(games_data)

    if df.empty:
        return None

    domestic_competitions_df = df[df['competition_type'] == 'domestic_league']

    games_per_year_country = domestic_competitions_df.groupby(['season', 'country'])['game_id'].nunique().reset_index()

    games_per_year_country['season'] = pd.to_datetime(games_per_year_country['season'], format='%Y')
    games_per_year_country.sort_values('season', inplace=True)

    # Set the figure size
    plt.figure(figsize=(16, 8))  # Width: 16 inches, Height: 8 inches
    cmap = mpl.colormaps['tab20b']
    num_countries = len(games_per_year_country['country'].unique())

    for i, country in enumerate(games_per_year_country['country'].unique()):
        country_data = games_per_year_country[games_per_year_country['country'] == country]
        if not country_data.empty:  # Ensure there's data to plot
            plt.plot(country_data['season'], country_data['game_id'], marker='x', label=country, color=cmap(i % num_countries))

    plt.title('Trends in the Number of Games Played by Country')
    plt.xlabel('Year')
    plt.ylabel('Number of Games Played')
    plt.xticks(rotation=45)
    plt.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid()
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png')


def world_map(db):
    games_collection = db['games']
    # Fetch all documents from the collection
    games_data = list(games_collection.find())

    # Convert the data to a DataFrame
    df = pd.DataFrame(games_data)

    # Count the number of games per country
    games_count = df['country'].value_counts().reset_index()
    games_count.columns = ['country', 'game_count']

    # Load world map data from the local shapefile
    world = gpd.read_file('data/naturalhearth/ne_110m_admin_0_countries.shp')  # Update the path accordingly

    # Merge the game count data with the world GeoDataFrame
    world = world.merge(games_count, how='left', left_on='ADMIN', right_on='country')  # Adjust 'ADMIN' to match the correct column name

    # Fill NaN values with 0 for countries with no games
    world['game_count'] = world['game_count'].fillna(0)

    # Get the list of countries with game_count > 0
    countries_with_games = world[world['game_count'] > 0]['country'].tolist()

    # Set the figure size
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))  # Set a specific size for the world map
    world.boundary.plot(ax=ax, linewidth=1)
    world.plot(column='game_count', ax=ax, legend=True,
               legend_kwds={'label': "Number of Games by Country",
                            'orientation': "horizontal"},
               cmap='OrRd', missing_kwds={"color": "lightgrey", "label": "No data"})

    # Title and display
    plt.title('Number of Games Played by Country', fontsize=15)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Save plot to BytesIO
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Encode image to Base64
    image_base64 = base64.b64encode(img.getvalue()).decode('utf-8')  # Convert to Base64 string

    # Return both the image and the list of countries
    response = {
        'countries_with_games': countries_with_games,
        'image': image_base64  # Use Base64 string for the image
    }

    return jsonify(response)  # Return as JSON
