# Imports the dependencies.
from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import pandas as pd
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflects the database into a new model
Base = automap_base()

# reflects the tables
Base.prepare(autoload_with=engine)

# Saves references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# [/] - Index with all the available routes.
@app.route("/")
def index():
    return """
    <html>
        <head>
            <style>
                body {
                    font-family: "Lucida Console", "Courier New", monospace;
                    }
                td {
                    padding: 15px;
                    }
            </style>
        </head>
    <body>
    <h1>Welcome to the Hawaii climate API</h1>
    <h2>Endpoints:</h2>
    <table border='1' style='border-collapse:collapse'>
        <tr style="border: 1px solid black;">
            <th>Endpoint</th>
            <th>Description</th>
        </tr>
        <tr>
            <td>/api/v1.0/precipitation</td>
            <td>Returns precipitation for the most recent year from availible data</td>
        </tr>
        <tr>
            <td>/api/v1.0/stations</td>
            <td>Returns a list of all weather stations</td>
        </tr>
        <tr>
            <td>/api/v1.0/tobs</td>
            <td>Returns the observed temperature and dates from the most recent year from availible data from the most active weather station in Hawaii(USC00519281)</td>
        </tr>
        <tr>
            <td>/api/v1.0/&lt;start&gt;</td>
            <td>Returns the min, max, and average temperature from the start date from the most active weather station in Hawaii(USC00519281)<br><b>Tip: Dates must be formatted as YYYY-MM-DD</b></td>
        </tr>
        <tr>
            <td>/api/v1.0/&lt;start&gt;/&lt;end&gt;</td>
            <td>Returns the min, max, and average temperature between the start and end dates from the most active weather station in Hawaii(USC00519281)<br><b>Tip: Dates must be formatted as YYYY-MM-DD</b></td>
        </tr>
        <tr>
            <td>/api/v1.0/&lt;station&gt;/tobs</td>
            <td>Returns the observed temperature and dates from the most recent year from availible data from the station specified in the URI<br><b>Tip: Use the /api/v1.0/tobs endpoint to return stations</b></td>
        </tr>
    </table>
    </body>
    """

# [/api/v1.0/precipitation] - 
# Converts the query results from the precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
# Returns the JSON representation of the dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    recent_rain = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').all()
    
    session.close()

    percip = []
    for date, prcp in recent_rain:
        percip_dict = {}
        percip_dict['date'] = date
        percip_dict['prcp'] = prcp
        percip.append(percip_dict)
    

    return jsonify(percip)


# [/api/v1.0/stations] - 
# Returns a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    station_query = session.query(Station.station, Station.name)
    session.close()

    stations = []
    for station, name in station_query:
        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name
        stations.append(station_dict)

    return jsonify(stations)



# [/api/v1.0/tobs] - 
# Queries the dates and temperature observations of the most-active station for the previous year of data.
# Returns a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    active_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()
    session.close()

    percip = []
    for date, prcp in active_query:
        percip_dict = {}
        percip_dict['date'] = date
        percip_dict['prcp'] = prcp
        percip.append(percip_dict)
    
    return jsonify(percip)


# [/api/v1.0/<start>] - 
# Returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start date.
# Calculates TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)

    recent_active = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= start).all()
    session.close()

    active_df = pd.DataFrame(recent_active)
    
    min_max_avg = {}
    min_active = active_df['tobs'].min()
    min_max_avg['min_temp'] = min_active
    max_active = active_df['tobs'].max()
    min_max_avg['max_temp'] = max_active
    mean_active = active_df['tobs'].mean()
    min_max_avg['avg_temp'] = mean_active
    return jsonify(min_max_avg)


# [/api/v1.0/<start>/<end>] - 
# Returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range.
# Calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route("/api/v1.0/<start>/<end>")
def start_edd(start, end):

    session = Session(engine)

    recent_active = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= start, Measurement.date <= end).all()
    session.close()

    active_df = pd.DataFrame(recent_active)
    
    min_max_avg = {}
    min_active = active_df['tobs'].min()
    min_max_avg['min_temp'] = min_active
    max_active = active_df['tobs'].max()
    min_max_avg['max_temp'] = max_active
    mean_active = active_df['tobs'].mean()
    min_max_avg['avg_temp'] = mean_active
    return jsonify(min_max_avg)

# [/api/v1.0/<station>/tobs] - 
# Returns a JSON list of temperature observations from the previous year from a specified station.
# Queries the dates and temperature observations of a specified station for the previous year of data.
# Note: This was not part of the assignment, but was something extra that I was testing...


@app.route("/api/v1.0/<station>/tobs")
def cust_tobs(station):

    session = Session(engine)

    active_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == station).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()
    session.close()

    percip = []
    for date, prcp in active_query:
        percip_dict = {}
        percip_dict['date'] = date
        percip_dict['prcp'] = prcp
        percip.append(percip_dict)
    
    return jsonify(percip)

if __name__ == '__main__':
    app.run(debug=True)