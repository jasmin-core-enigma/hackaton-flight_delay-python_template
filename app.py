import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

def get_flight_data():
    df = pd.read_csv('data/flights.csv')
    origin_cities = df['OriginCity'].unique()
    dest_cities = df['DestCity'].unique()
    flight_data = df[['OriginCity', 'DestCity', 'CRSDepTime', 'CRSArrTime']].drop_duplicates()
    return origin_cities, dest_cities, flight_data

def format_time(time):
    time_str = str(int(time)).zfill(4)  # Ensure time is in HHMM format
    return f"{time_str[:2]}:{time_str[2:]}"

@app.route("/")
def index():
    origin_cities, dest_cities, _ = get_flight_data()
    return render_template("index.html", origin_cities=origin_cities, dest_cities=dest_cities)

@app.route("/submit", methods=["POST"])
def submit():
    departure = request.form["departure"]
    destination = request.form["destination"]
    date = request.form["date"]
    
    _, _, flight_data = get_flight_data()
    valid_combination = flight_data[(flight_data['OriginCity'] == departure) & (flight_data['DestCity'] == destination)]
    
    if not valid_combination.empty:
        dep_time = format_time(valid_combination.iloc[0]['CRSDepTime'])
        arr_time = format_time(valid_combination.iloc[0]['CRSArrTime'])
        return render_template("response.html", departure=departure, destination=destination, date=date, dep_time=dep_time, arr_time=arr_time)
    else:
        return render_template("response.html", error="Invalid city combination. Please pick again.")

if __name__ == "__main__":
    app.run(debug=True)