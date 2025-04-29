from flask import Flask, jsonify
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load CSV data at startup
csv_file = "final_schedule.csv"
df = pd.read_csv(csv_file)

# Convert datetime column to pandas datetime format
df["Datetime"] = pd.to_datetime(df["Datetime"])

# Function to get appliance status based on current time
def get_appliance_status(appliance):
    current_time = datetime.now().strftime("%Y-%m-%d %H:00")
    
    # Find the row matching current time
    row = df[df["Datetime"].dt.strftime("%Y-%m-%d %H:00") == current_time]
    
    if not row.empty:
        status = row[appliance].values[0]
        return status
    else:
        return "UNKNOWN"  # If time not found in CSV


# **API Endpoints for each appliance**
@app.route('/status/refrigerator')
def refrigerator_status():
    return jsonify({"status": get_appliance_status("Refrigerator")})

@app.route('/status/ac')
def ac_status():
    return jsonify({"status": get_appliance_status("Air Conditioner")})

@app.route('/status/lights')
def lights_status():
    return jsonify({"status": get_appliance_status("Lights")})

@app.route('/status/fans')
def fans_status():
    return jsonify({"status": get_appliance_status("Fans")})

@app.route('/status/tv')
def tv_status():
    return jsonify({"status": get_appliance_status("Television")    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=True)