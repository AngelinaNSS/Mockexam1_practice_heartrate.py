from flask import Flask, render_template
import json
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/")
def index():
    # Load heart rate data from JSON file
    with open('heart_rate_data.json') as f:
        data = json.load(f)

    # Get the current time and the time 2 hours ago
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=2)

    heart_rates = []

    # Extract heart rate data for the latest 2-hour interval
    for entry in data:
        entry_start = datetime.fromisoformat(entry['startTimestampLocal'])
        entry_end = datetime.fromisoformat(entry['endTimestampLocal'])

        # Check if the entry falls within the last 2 hours
        if entry_end > start_time and entry_start < end_time:
            heart_rates.extend(value[1] for value in entry['heartRateValues'] if value[1] is not None)

    # Calculate min, max, and average heart rate
    if heart_rates:
        min_hr = min(heart_rates)
        max_hr = max(heart_rates)
        avg_hr = sum(heart_rates) / len(heart_rates)
    else:
        min_hr, max_hr, avg_hr = None, None, None

    return render_template("index.html", min_hr=min_hr, max_hr=max_hr, avg_hr=avg_hr)

if __name__ == "__main__":
    app.run(debug=True)
