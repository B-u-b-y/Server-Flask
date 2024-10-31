from flask import Flask, jsonify, send_file
from flask_cors import cross_origin
from database.db import get_db_connection
from service.appearances import player_statistics
from service.games import test_method, world_map  # Import world_map

app = Flask(__name__)

db = get_db_connection()

@app.route("/test", methods=['POST'])
@cross_origin(origin="http://localhost:3000")
def test():
    print("test")
    result = test_method(db)  # Call the test_method and capture the result
    if result is None:
        return jsonify({"error": "No data found in the collection."}), 404  # Return a JSON response if no data found
    return result  # Return the plot directly

@app.route("/world-map", methods=['POST'])  # Create a new route for the world map
@cross_origin(origin="http://localhost:3000")
def get_world_map():
    print("Generating world map")
    result = world_map(db)  # Call the world_map function
    if result is None:
        return jsonify({"error": "No data found in the collection."}), 404  # Return a JSON response if no data found
    return result  # Return the map image directly

@app.route("/player-stats", methods=['POST'])  # Create a new route for the world map
@cross_origin(origin="http://localhost:3000")
def player_stats():
    print("Generating player stats")
    result = player_statistics(db)  # Call the world_map function
    if result is None:
        return jsonify({"error": "No data found in the collection."}), 404  # Return a JSON response if no data found
    return result  # Return the map image directly


if __name__ == '__main__':
    app.run(port=8092, debug=True)
